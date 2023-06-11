import typing
from datetime import datetime

from .base import SmartixModel
from .common import PointTypeEnum, StateEnum, VPNModeEnum


class ControllerState(SmartixModel):
    id: int
    state: int
    number: int
    postamat_id: int
    point_id: int


class Object(SmartixModel):
    id: int
    name: str
    title: str
    state: typing.Union[
        typing.Literal[StateEnum.ACTIVE], typing.Literal[StateEnum.HIDDEN]
    ]
    last_connection: datetime
    last_payload: datetime
    update_app_active: bool
    update_res_active: bool
    vpn_mode: typing.Union[
        typing.Literal[VPNModeEnum.ON], typing.Literal[VPNModeEnum.OFF]
    ]
    demon_version: str
    demon_date_build: datetime
    gui_version: str
    gui_date_build: datetime
    id_organization: int
    organization: str
    full_addres: str
    temporary_blocking: bool
    last_connection_time: int
    last_payload_time: int
    apo_point_type: bool
    tun_0_ip: str
    free_disk_space: int
    cpu_temp: int
    gui_status: int
    offline_packet_error_count: int
    controller_states: typing.List[ControllerState]
    has_point_box: bool
    point_type: typing.Literal[PointTypeEnum.POSTAMAT]
