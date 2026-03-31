from fastapi import FastAPI

#from app.database.qdrant import initialize_qdrant
#from app.routes import search
#from app.services import qdrant_service

app = FastAPI()

#app.include_router(search.router)
#app.include_router(qdrant_service.router)

def background_init():
    print("Initializing Qdrant in background...")
    initialize_qdrant()
    print("Qdrant Ready ✅")


#@app.on_event("startup")
#def start_background_task():
    thread = threading.Thread(target=background_init)
    thread.start()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"messages": f"Hello {name}"}
