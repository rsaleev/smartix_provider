import typing
from typing_extensions import Literal

from datetime import datetime

from .common import PointTypeEnum, SmartixModel, StateEnum


class PostamatDetailed(SmartixModel):
    id: str
    date_create: datetime
    state: typing.Union[
        Literal[StateEnum.ACTIVE], Literal[StateEnum.HIDDEN]
    ]
    use_for_delivery: bool
    use_for_returning: bool
    use_for_c2C: bool
    use_for_rent: bool
    use_for_paid_storage: bool
    use_for_free_loads: bool
    model_profile_id: int
    model_profile_name: str
    postamat_profile_id: int
    postamat_profile_name: str
    delivery_order_extension_interval: int
    reserve_factor: int


class Postamat(SmartixModel):
    id: int
    name: str
    title: str
    date_update: datetime
    state: typing.Union[
        Literal[StateEnum.ACTIVE], Literal[StateEnum.HIDDEN]
    ]
    date_create: datetime
    api_key: str
    static_key: str
    dynamic_key: bool
    find: str
    lock_desktop_on_keyboard: bool
    access_guide: str
    for_test: bool
    publish: bool
    auto_update: bool
    organization_id: int
    organization_name: str
    location_id: int
    location_name: str
    language_profile_id: int
    language_profile_name: str
    application_id: int
    application_name: str
    point_type: Literal[PointTypeEnum.POSTAMAT]
    point_view_id: int
    point_view_name: str
    postamat: PostamatDetailed
    group_name: str


class Courier(SmartixModel):
    id:int 
    organization_id:int
    person_id:int
    person_name:str
    postamat_permission_profile_id:int
    postamat_permission_profile_name:str
    group_name:str


class ModelProfile(SmartixModel):
    id:int
    name:str
    active:bool
    organization_id:int
    organization_name:str
    controller_type_id:int
    controller_type_name:str
    max_lines_count:int
    controller_count:int
    locker_count:int
    cell_count:int
    cell_temp_count:int
    max_weight:int
    cell_max_size:str
    cell_min_size:str
    disabled:bool