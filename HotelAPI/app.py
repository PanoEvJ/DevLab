import contextlib

import uvicorn
from fastapi import FastAPI

from hotel.db.engine import init_db
from hotel.routers import customers, rooms

DB_FILE = "sqlite:///hotel.db"


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db(DB_FILE)
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return "The server is running"


app.include_router(rooms.router)
app.include_router(customers.router)
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
