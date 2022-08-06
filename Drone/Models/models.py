from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from typing import List


class ModelDrone(str, Enum):
    lightweight = 'Lightweight'
    middleweight = 'Middleweight'
    cruiserweight = 'Cruiserweight'
    heavyweight = 'Heavyweight'


class State(str, Enum):
    idle = 'IDLE'
    loading = 'LOADING'
    loaded = 'LOADED'
    delivering = 'DELIVERING'
    delivered = 'DELIVERED'
    returning = 'RETURNING'


class Medication(BaseModel):
    id: Optional[str]
    name: str
    weight: int
    code: str
    image: str


class Drone(BaseModel):
    id: Optional[str]
    serial_number: str = Field(
        min_length = 0,
        max_length = 100
    )
    model: ModelDrone
    weight_limit: float = Field(
        exclusiveMaximum = 500
    )
    battery_capacity: float
    state: State
    # medication: List[Medication]
