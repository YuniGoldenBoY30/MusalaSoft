from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from schemas.medication import Medication


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


class Drone(BaseModel):
    id: int
    serial_number: str = Field(
        min_length=0,
        max_length=100
    )
    model: ModelDrone
    weight_limit: float = Field(
        exclusiveMaximum=500
    )
    battery_capacity: float = 100.0
    state: State
    medications: list[Medication] = []

    class Config:
        orm_mode = True


class DroneUpdate(BaseModel):
    serial_number: str


class DroneGet(BaseModel):
    serial_number: str


class Response(BaseModel):
    message: str
