from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from schemas.database import Base


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


class Drone(Base):
    __tablename__ = "drones"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    serial_number = Column(String(100), unique=True)
    model = Column(String, nullable=False, default="Lightweight")
    weight_limit = Column(Float(500))
    battery_capacity = Column(Float(100))
    state = Column(String, nullable=False, default="IDLE")
    medications = relationship("Medication", back_populates="drone")


class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    weight = Column(Integer)
    code = Column(String(255))
    image = Column(String, nullable=True)
    drone_id = Column(Integer, ForeignKey("drones.id"))
    drone = relationship("Drone", back_populates="medications")
