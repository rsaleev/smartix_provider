import typing
from datetime import datetime
from enum import Enum

from .base import SmartixModel


def ts_to_dt(arg: int):
    return datetime.fromtimestamp(arg)


class StateEnum(Enum):
    ACTIVE = "active"
    HIDDEN = "blocked"


class VPNModeEnum(Enum):
    ON = "ON"
    OFF = "OFF"


class PointTypeEnum(Enum):
    POSTAMAT = "POSTAMAT"


class RequestParams(SmartixModel):
    page: int = 0
    size: int = 50
