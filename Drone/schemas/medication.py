from typing import Optional

from pydantic import BaseModel


class Medication(BaseModel):
    id: int
    name: str
    weight: int
    code: str
    image: Optional[str]
    drone_id: int

    class Config:
        orm_mode = True


class MedicationUpdate(BaseModel):
    name: str


class MedicationGet(BaseModel):
    name: str


class Response(BaseModel):
    message: str
