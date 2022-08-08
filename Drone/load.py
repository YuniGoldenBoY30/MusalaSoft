import csv

from sqlalchemy.exc import IntegrityError

import models.models as model
from schemas.database import Sesionlocal, engine

db = Sesionlocal()

model.Base.metadata.create_all(bind=engine)
try:
    with open("models/data/dataset_drone.csv", "r") as f:
        csv_reader = csv.DictReader(f, delimiter=';')
        for row in csv_reader:
            wl = float(row["weight_limit"])
            if wl > 500:
                print("Weight limit of 500gr max")
                wl = 500
            db_record = model.Drone(
                id=int(row["id"]),
                serial_number=row["serial_number"],
                model=row["model"],
                weight_limit=float(wl),
                battery_capacity=float(row["battery_capacity"]),
                state=row["state"],
                medications=list(row["medications"])
            )
            db.add(db_record)

        db.commit()

    with open("models/data/dataset_medication.csv", "r") as f:
        csv_reader = csv.DictReader(f, delimiter=';')
        for row in csv_reader:
            drone_medication = db.query(model.Drone).filter(model.Drone.id == int(row["drone_id"])).first()
            capacity = drone_medication.weight_limit - int(row["weight"])
            if capacity > 0:
                drone_medication.state = "LOADING"
            elif capacity == 0:
                drone_medication.state = "LOADED"
            else:
                print("The load exceeded the capacity of the drone")
                exit(1)
            db_record = model.Medication(
                id=int(row["id"]),
                name=row["name"],
                weight=int(row["weight"]),
                code=row["code"],
                image=row["image"],
                drone_id=int(row["drone_id"])
            )
            drone_medication.weight_limit = capacity
            db.add(db_record)
            db.add(drone_medication)

        db.commit()
        db.refresh(db_record)
        db.refresh(drone_medication)

    db.close()

    print("Drone and medication data successfully loaded!")
except IntegrityError as e:
    print("Data already inserted, please check 'drone.db' file!")
    pass
except Exception as e:
    print("Try Again")
    print(str(e))
