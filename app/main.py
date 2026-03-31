from fastapi import FastAPI
import threading

from app.database.qdrant import initialize_qdrant

app = FastAPI()

def background_init():
    print("Initializing Qdrant in background...")
    initialize_qdrant()
    print("Qdrant Ready ✅")

@app.on_event("startup")
async def start_background_task():
    thread = threading.Thread(target=background_init)
    thread.start()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}