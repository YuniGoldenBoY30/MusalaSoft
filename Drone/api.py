from fastapi import FastAPI
from Models.models import Drone, Medication
from uuid import uuid4 as uid

app = FastAPI()
drones_db = []


@app.get("/")
async def root():
    return {"message": "Stand up"}


@app.get("/drone/{drone_id}")
async def get_drone_by_id(drone_id):
    for drone in drones_db:
        if drone["id"] == drone_id:
            return {"drone": drone}
        return "not found"


@app.get("/drones")
async def get_all_drone():
    return drones_db


@app.post("/drone")
def save_drone(drone: Drone):
    drone.id = str(uid())
    drones_db.append(drone.dict())
    return drones_db


@app.delete("/drone/{drones_id}")
def delete_drone(drone: str):
    for (k, v) in enumerate(drones_db):
        print(k, v)
    return "detelted"
