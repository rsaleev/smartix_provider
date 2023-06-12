import typing
from contextlib import contextmanager

import tenacity
from airflow.exceptions import AirflowNotFoundException
from airflow.hooks.base import BaseHook
from requests import ConnectionError, ConnectTimeout, Response, Session

from ..models.common import RequestParams
from ..models.delivery import PostOperation
from ..models.monitoring import Object
from ..models.postamats import Courier, ModelProfile, Postamat
from ..models.reports import ProblemCell
from ..models.settings import Location, Organization


class SmartixHook(BaseHook):
    conn_name_attr = "smartix_conn_id"
    default_conn_name = "smartix_default"
    conn_type = "http"
    hook_name = "SMARTIX"

    def __init__(self, smartix_conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.smartix_conn_id = smartix_conn_id
        self.retry_obj = tenacity.Retrying(
            stop=tenacity.stop_after_attempt(3),
            retry=tenacity.retry_if_exception_type(
                (
                    ConnectionError,
                    ConnectTimeout,
                )
            ),
        )
        self.base_url: str = ""

    def get_conn(self) -> Session:
        session = Session()
        conn = self.get_connection(self.smartix_conn_id)
        if not conn.host:
            raise AirflowNotFoundException("Connection requires host")
        self.base_url = conn.host
        if not conn.login:
            raise AirflowNotFoundException(f"Connection {conn.host} requires login")
        if not conn.password:
            raise AirflowNotFoundException(f"Connection {conn.host} requires password")
        self.__auth(session, conn.login, conn.password)
        return session

    def __auth(self, session: Session, login: str, password: str):
        url = f"{self.base_url}/login"
        r = session.post(
            url, data={"username": login, "password": password, "remember-me": "on"}
        )
        r.raise_for_status()

    def __get_total_items(self, r: Response):
        total_items = RequestParams().size
        if r.headers.get("x-total-count"):
            total_items = int(r.headers["x-total-count"])
        else:
            payload = r.json()
            if payload.get("totals"):
                if payload["totals"].get("totalRecords"):
                    total_items = payload["totals"]["totalRecords"]
        return total_items

    def __fetch_all(
        self,
        endpoint: str,
        **kwargs,
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        session = self.get_conn()
        payload = []
        request_params = RequestParams()
        params = request_params.dict(by_alias=True)
        params.update(kwargs)
        r = session.get(f"{self.base_url}/{endpoint}", params=params)
        self.log.info(f"{r.request.method} {r.request.url} {r.status_code}")
        r.raise_for_status()
        total_items = self.__get_total_items(r)
        self.log.info(f"TOTAL ITEMS {total_items}")
        total_pages = total_items // request_params.size - 1
        self.log.info(f"TOTAL PAGES {total_pages}")
        data = r.json()["data"]
        if isinstance(data, dict) and data.get("items"):
            payload.extend(data["items"])
            return payload
        payload.extend(data)
        for i in range(1, total_pages):
            request_params.page = i
            params = request_params.dict(by_alias=True)
            params.update(kwargs)
            r = session.get(f"{self.base_url}/{endpoint}", params=params)
            payload.extend(r.json()["data"])
        session.close()
        return payload

    def __fetch_one(self, endpoint: str, **kwargs) -> typing.Dict[str, typing.Any]:
        session = self.get_conn()
        request_params = RequestParams()
        params = request_params.dict(by_alias=True)
        params.update(kwargs)
        r = session.get(f"{self.base_url}/{endpoint}", params=params)
        self.log.info(f"{r.request.method} {r.request.url} {r.status_code}")
        r.raise_for_status()
        payload = r.json()["data"]
        session.close()
        return payload

    def get_problemcells(self, **kwargs) -> typing.List[ProblemCell]:
        endpoint = f"report/postamat-cell/problem"
        data = self.retry_obj(self.__fetch_all, endpoint=endpoint, **kwargs)
        items = data["items"]  # type: ignore
        return [ProblemCell.parse_obj(item) for item in items]

    def get_monitoring(self, **kwargs) -> typing.List[Object]:
        endpoint = f"monitoring"
        data = self.retry_obj(self.__fetch_all, endpoint=endpoint, **kwargs)
        return [Object.parse_obj(item) for item in data]

    def get_postamats(self, **kwargs) -> typing.List[Postamat]:
        endpoint = f"postamat"
        data = self.retry_obj(self.__fetch_all, endpoint=endpoint, **kwargs)
        return [Postamat.parse_obj(item) for item in data]

    def get_organizations(self, **kwargs) -> typing.List[Organization]:
        endpoint = f"organization"
        data = self.retry_obj(self.__fetch_all, url=endpoint, **kwargs)
        return [Organization.parse_obj(item) for item in data]

    def get_locations(self, **kwargs) -> typing.List[Location]:
        endpoint = f"location"
        data = self.retry_obj(self.__fetch_all, endpoint, **kwargs)
        return [Location.parse_obj(item) for item in data]

    def get_location_detail(self, id: int, **kwargs) -> Location:
        endpoint = f"location/{id}"
        data = self.retry_obj(self.__fetch_one, endpoint, **kwargs)
        return Location.parse_obj(data)

    def get_couriers(self, **kwargs) -> typing.List[Courier]:
        endpoint = f"courier"
        data = self.retry_obj(self.__fetch_all, endpoint, **kwargs)
        return [Courier.parse_obj(item) for item in data]

    def get_orders(self, **kwargs) -> list:
        raise NotImplementedError

    def get_profit(self, **kwargs):
        """
        Расчитывает баланс операций при захардкоженых id организаций. см код метода.
        """
        endpoint = f"post-operation-calc-report"
        d = self.retry_obj(self.__fetch_all, endpoint, **kwargs)
        if not d:
            return 0
        sum = 0
        for t in d:
            if t["organizationFromId"] == 1:  # Московский почтомат(Система)
                if t["organizationToId"] != 5:  # Московский почтомат
                    sum -= t["sumValue"]
            elif t["organizationToId"] == 1:
                sum += t["sumValue"]
        return sum / 100

    def get_operation_count(self, **kwargs):
        endpoint = f"post-operation-calc-report"
        data = self.retry_obj(self.__fetch_all, endpoint, **kwargs)
        if not data:
            return 0
        operations = set()
        for o in data:
            operations.add(o["postOperationId"])
        return len(operations)

    def get_modelprofile_detail(self, model_profile_id: int, **kwargs) -> ModelProfile:
        endpoint = f"model-profile/{model_profile_id}"
        data = self.retry_obj(self.__fetch_one, endpoint, **kwargs)
        return ModelProfile.parse_obj(data)

    def get_operation(self, **kwargs) -> list:
        endpoint = f"post-operation"
        data = self.retry_obj(self.__fetch_one, endpoint, **kwargs)
        return [PostOperation.parse_obj(item) for item in data]

    def get_operation_detail(self, id: int, **kwargs):
        raise NotImplementedError
