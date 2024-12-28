import uvicorn
from fastapi import FastAPI

from hotel.db.engine import init_db

app = FastAPI()

DB_FILE = "sqlite:///hotel.db"


@app.on_event("startup")
def startup():
    init_db(DB_FILE)


@app.get("/")
def read_root():
    return "The server is running"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
