from fastapi import FastAPI
from starlette.responses import RedirectResponse

import models.models as create_model
from routes.drone import router_drone
from routes.medication import router_medication
from schemas.database import engine

create_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Api Drone",
              description="simple rest-full api with sqlite",
              version="1.0")

app.include_router(router_drone)
app.include_router(router_medication)


# route index to redirect a documentation
@app.get("/")
async def main():
    return RedirectResponse(url="/docs/")
