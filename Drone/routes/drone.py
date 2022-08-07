from uuid import uuid4 as uid

from fastapi import APIRouter

from schemas.database import Sesionlocal
from schemas.drone import Drone

router_drone = APIRouter(prefix="/drone")

drones_db = []
medication_db = []


# retorna la conexion con una sesion
def get_db():
    try:
        db = Sesionlocal()
        yield db
    finally:
        db.close()


# @router_drone.get("/prueba")
# async def pruebaProduct(db: Session = Depends(get_db)):
#     return "success, in process Drone"

#
@router_drone.post("/create")
def save_drone(drone: Drone):
    """
    * registering a drone;
    * loading a drone with medication items;
    """
    drone.id = str(uid())
    drones_db.append(drone.dict())
    return drones_db


@router_drone.get("/get-drone/{drone_id}")
async def get_drone_by_id(drone_id):
    """
        * Get all information about a given drone
    """
    for drone in drones_db:
        if drone["id"] == drone_id:
            return {"drone": drone}
        return "not found"


@router_drone.get("/loaded-medication/{drone_id}")
async def check_loaded_medication(drone_id):
    """
        * checking loaded medication items for a given drone
    """
    return "check_loaded_medication"


@router_drone.get("/availables-drones/")
async def check_available_drones():
    """
        * checking available drones for loading
    """
    return "check_available_drones"


@router_drone.get("/battery-level/{drone_id}")
async def check_battery_level(drone_id):
    """
        * check drone battery level for a given drone
    """
    for drone in drones_db:
        if drone["id"] == drone_id:
            return {"drone": drone["battery_capacity"]}
        return "NOT FOUND DRONE"


@router_drone.get("/list")
async def get_all_drone():
    """
        * check all drone
    """
    return drones_db

#
# @router_drone.post("/medication")
# def save_medication(medication: Medication):
#     medication.id = str(uid())
#     medication_db.append(medication.dict())
#     return medication_db
