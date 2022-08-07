from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import models
from schemas import drone, medication


def get_all_drone(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Drone).offset(skip).limit(limit).all()


def get_drone_by_id(db: Session, drone_id: int):
    return db.query(models.Drone).filter(models.Drone.id == drone_id).first()


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
    db_medications = models.Medication(**medications.dict())
    db.add(db_medications)
    db.commit()
    db.refresh(db_medications)
    return db_medications
