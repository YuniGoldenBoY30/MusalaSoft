from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from schemas.database import Sesionlocal

# objeto tipó APIRouter
router_medication = APIRouter(prefix="/medication")


# retorna la conexion con una sesion
def get_db():
    try:
        db = Sesionlocal()
        yield db
    finally:
        db.close()


@router_medication.get("/med")
async def pruebaMed(db: Session = Depends(get_db)):
    return "success, in process Med"
