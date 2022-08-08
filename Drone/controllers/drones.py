from uuid import uuid4 as uid

from fastapi import HTTPException
from sqlalchemy.orm import Session

# from fastapi.encoders import jsonable_encoder
from models import models
from schemas import drone, medication


def get_all_drone(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Drone).offset(skip).limit(limit).all()


def get_drone_by_id(db: Session, drone_id: str):
    try:
        return db.query(models.Drone).filter(models.Drone.id == drone_id).first()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def create_drone(db: Session, drones: drone.Drone):
    try:
        db_drones = models.Drone(**drones.dict())
        db.add(db_drones)
        db.commit()
        db.refresh(db_drones)
        return db_drones
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def create_drone_medications(db: Session, medications: medication.Medication):
    drone_medication = db.query(models.Drone).filter(models.Drone.id == medications.drone_id).first()
    capacity = drone_medication.weight_limit - medications.weight
    if drone_medication.battery_capacity < 25:
        raise HTTPException(status_code=404,
                            detail=f"Low Battery at {drone_medication.battery_capacity}, please recharge")
    if capacity > 0:
        drone_medication.state = "LOADING"
    elif capacity == 0:
        drone_medication.state = "LOADED"
    else:
        raise HTTPException(status_code=404, detail="The load exceeded the capacity of the drone")

    db_medications = models.Medication(**medications.dict())
    db.add(db_medications)
    drone_medication.weight_limit = capacity
    db.add(drone_medication)
    db.commit()
    db.refresh(db_medications)
    db.refresh(drone_medication)
    return db_medications


def check_loaded_medication(drone_id: str, db: Session):
    try:
        list_medications = db.query(models.Drone).filter(models.Drone.id == drone_id).first().medications
        return {"detail": list_medications} if len(list_medications) > 0 else {"detail": "Drone empty !"}
    except AttributeError as exc:
        raise HTTPException(status_code=404, detail="Drone not found !")


def check_available_drones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Drone).filter(models.Drone.state == "IDLE").offset(skip).limit(limit).all()


def check_battery_level(drone_id: str, db: Session):
    try:
        data = db.query(models.Drone).filter(models.Drone.id == drone_id).first().battery_capacity
        return {"battery_capacity": data}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
