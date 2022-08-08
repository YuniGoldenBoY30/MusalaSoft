from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers import drones as drones_controller
from schemas import drone as sch_drone, medication as sch_med
from schemas.database import Sesionlocal

router_drone = APIRouter(prefix="/drone")


# retorna la conexion con una sesion
def get_db():
    try:
        db = Sesionlocal()
        yield db
    finally:
        db.close()


@router_drone.post("/create/", response_model=sch_drone.Drone)
async def create_drone(drone: sch_drone.Drone, db: Session = Depends(get_db)):
    """
        * registering a drone
    """
    db_drone = drones_controller.get_drone_by_id(db, drone.id)
    if db_drone:
        raise HTTPException(status_code=404, detail="Drone already registered !")
    return drones_controller.create_drone(db=db, drones=drone)


@router_drone.post("/create/{drone_id}/medications/")
async def create_medications_for_drone(medications: sch_med.Medication, db: Session = Depends(get_db)):
    """
        * loading a drone with medication items
    """
    db_drone = drones_controller.get_drone_by_id(db, medications.drone_id)
    if not db_drone:
        raise HTTPException(status_code=404, detail="Drone not found !")
    return drones_controller.create_drone_medications(db=db, medications=medications)


@router_drone.get("/get-drone/{drone_id}/", response_model=sch_drone.Drone)
async def get_drone_by_id(drone_id: str, db: Session = Depends(get_db)):
    """
        * Get all information about a given drone
    """
    db_drone = drones_controller.get_drone_by_id(db, drone_id)
    if not db_drone:
        raise HTTPException(status_code=404, detail="Drone not found !")
    return db_drone


@router_drone.get("/loaded-medication/{drone_id}/", )
async def check_loaded_medication(drone_id: str, db: Session = Depends(get_db)):
    """
        * checking loaded medication items for a given drone
    """
    load_medications = drones_controller.check_loaded_medication(db=db, drone_id=drone_id)
    if load_medications is None:
        raise HTTPException(status_code=404, detail="Drone not found !")
    return load_medications


@router_drone.get("/available-drones/", response_model=list[sch_drone.Drone])
async def check_available_drones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
        * checking available drones for loading
    """
    list_drones = drones_controller.check_available_drones(db, skip, limit)
    return list_drones


@router_drone.get("/battery-level/{drone_id}/")
async def check_battery_level(drone_id: str, db: Session = Depends(get_db)):
    """
        * check drone battery level for a given drone
    """
    db_drone = drones_controller.check_battery_level(db=db, drone_id=drone_id)
    if db_drone is None:
        raise HTTPException(status_code=404, detail="Drone not found !")
    return db_drone


@router_drone.get("/list/", response_model=list[sch_drone.Drone])
async def get_all_drone(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
        * check all drone
    """
    list_drones = drones_controller.get_all_drone(db, skip, limit)
    return list_drones
