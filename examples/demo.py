import random
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional


class Application(BaseModel):
    first_name: str
    last_name: str
    age: int
    degree: str
    interest: Optional[str] = None


class Decision(BaseModel):
    first_name: str
    last_name: str
    probability: float
    acceptance: bool


app = FastAPI()


@app.post("/applications", response_model=Decision)
async def create_application(id: int, application: Application):
    first_name = application.first_name
    last_name = application.last_name
    proba = random.random()
    acceptance = proba > 0.5

    decision = {
        "first_name": first_name,
        "last_name": last_name,
        "probability": proba,
        "acceptance": acceptance,
    }
    return decision


@app.get("/ids/")
async def read_ids(id: int):
    response = {"id": id}
    return response


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50, min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
