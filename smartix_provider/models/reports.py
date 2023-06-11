import typing
from datetime import datetime

from .base import SmartixModel
from .common import PointTypeEnum, StateEnum, VPNModeEnum


class ProblemCell(SmartixModel):
    id:int 
    title:str
    organization_id:int
    organization_name:str
    point_id:int 
    point_name:str
    front_cleaning_require:bool
    front_overflow:bool
    front_other:bool
    front_defective:bool
    front_busy:bool
    front_opened:bool
    front_for_inventory:bool


    