from fastapi import FastAPI
import threading


from app.routes import search 
from app.services import qdrant_service 
from app.database.qdrant import initialize_qdrant

app = FastAPI()

app.include_router(search.router) 
app.include_router(qdrant_service.router)

# 🔥 Background Initialization (Non-blocking)
def background_init():
    try:
        print("Initializing Qdrant in background...")
        initialize_qdrant()
        print("Qdrant Ready ✅")
    except Exception as e:
        print("Qdrant Init Error:", e)


# 🚀 Startup Event (Render-safe)
@app.on_event("startup")
async def start_background_task():
    thread = threading.Thread(target=background_init, daemon=True)
    thread.start()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}