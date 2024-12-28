from dataclasses import dataclass

import uvicorn
from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def read_root():
    return "The server is running"


@app.get("/customers")
def read_customers():
    return [
        Customer(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
