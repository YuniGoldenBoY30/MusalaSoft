from typing import Optional

from pydantic import BaseModel, validator, PydanticValueError


class NotValidEntry(PydanticValueError):
    msg_template = 'not valid entry, got "{wrong_value}"'


class Medication(BaseModel):
    id: int
    name: str
    weight: int
    code: str
    image: Optional[str]
    drone_id: int
    
    class Config:
        orm_mode = True
    
    @validator('name')
    def valid_name(cls, name):
        name = str(name).strip().lower()
        
        for letter in name:
            criteria = (
                letter.isalnum(),
                letter == "-",
                letter == "_"
            )
            if not any(criteria):
                raise NotValidEntry(wrong_value = name)
        return name
    
    @validator('code')
    def valid_code(cls, code):
        code = str(code).strip().upper()
        
        for letter in code:
            criteria = (
                letter.isalnum(),
                letter == "_",
            )
            if not any(criteria):
                raise NotValidEntry(wrong_value = code)
        return code


class MedicationUpdate(BaseModel):
    name: str


class MedicationGet(BaseModel):
    name: str


class Response(BaseModel):
    message: str
