from fastapi import FastAPI

from app.database.qdrant import initialize_qdrant
from app.routes import search
from app.services import qdrant_service

app = FastAPI()

app.include_router(search.router)
app.include_router(qdrant_service.router)


@app.on_event("startup")
async def startup_event() -> None:
    initialize_qdrant()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
