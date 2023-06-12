import typing
from datetime import datetime

from typing_extensions import Literal

from .base import SmartixModel
from .common import PointTypeEnum, StateEnum, VPNModeEnum


class ControllerState(SmartixModel):
    id: int
    state: int
    number: int
    postamat_id: int
    point_id: int


class DeviceState(SmartixModel):
    device_class: typing.Optional[int]
    device_number: typing.Optional[int]
    state: typing.Optional[int]
    flags: typing.Optional[int]
    point_id: typing.Optional[int]
    error: bool
    warning: bool
    critical_warning: bool


class Object(SmartixModel):
    id: int
    name: str
    title: typing.Optional[str]
    state: typing.Union[Literal[StateEnum.ACTIVE], Literal[StateEnum.HIDDEN]]
    last_connection: datetime
    last_payload: typing.Optional[datetime]
    update_app_active: bool
    update_res_active: bool
    vpn_mode: typing.Union[Literal[VPNModeEnum.ON], Literal[VPNModeEnum.OFF]]
    demon_version: str
    demon_date_build: datetime
    gui_version: str
    gui_date_build: datetime
    id_organization: int
    organization: str
    full_address: str
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
    device_states: typing.Optional[typing.List[DeviceState]]
    has_point_box: bool
    point_type: Literal[PointTypeEnum.POSTAMAT]
