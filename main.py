# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"testing": "CI/CD"}

@app.get("/portfolio/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
