import uvicorn
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

import models.models as create_model
from routes.drone import router_drone
from schemas.database import engine, SessionLocal

create_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Api Drone",
              description="simple rest-full api with sqlite",
              version="1.0")
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_drone)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# route index to redirect a documentation
@app.get("/")
async def main():
    return RedirectResponse(url="/docs/")


if __name__ == "__main__":
    try:
        exec(open("load.py").read())
        exec(open("logs/check_battery.py").read())
        uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="info")
    except Exception as e:
        print("FATAL ERROR")
        exit(-1)
