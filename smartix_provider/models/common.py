import typing
from enum import StrEnum

from .base import SmartixModel

from datetime import datetime

def ts_to_dt(arg:int):
    return datetime.fromtimestamp(arg)

class StateEnum(StrEnum):
    ACTIVE = "active"
    HIDDEN = "blocked"

class VPNModeEnum(StrEnum):
    ON = "ON"
    OFF = "OFF"

class PointTypeEnum(StrEnum):
    POSTAMAT = "POSTAMAT"

class RequestParams(SmartixModel):
    page: int = 0
    size: int = 50
 

