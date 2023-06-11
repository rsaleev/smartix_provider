from enum import Enum

from .base import BaseModel


class StateEnum(str, Enum):
    ACTIVE = "ACTIVE"
    HIDDEN = "BLOCKED"


class VPNModeEnum(str, Enum):
    ON = "ON"
    OFF = "OFF"


class PointTypeEnum(str, Enum):
    POSTAMAT = "POSTAMAT"


class RequestParams(BaseModel):
    page: int = 0
    size: int = 50
