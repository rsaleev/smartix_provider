import typing
from datetime import datetime

from .base import SmartixModel
from .common import StateEnum


class Organization(SmartixModel):
    id: int
    name: str
    state: typing.Union[
        typing.Literal[StateEnum.ACTIVE], typing.Literal[StateEnum.HIDDEN]
    ]
    date_create:datetime
    type:str
    default_timezone:str
    order:int
    language_id:int
    language_name:str

class Location(SmartixModel):
    id:int
    name:str
    city:str
    full_address:str
    work_time_profile_name:str
    organization_name:str
    state: typing.Union[
        typing.Literal[StateEnum.ACTIVE], typing.Literal[StateEnum.HIDDEN]
    ]
    group_name:str