from typing import Any
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

db = {
    1234: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed"
    },
    1235: {
        "weight": 1.2,
        "content": "electronics",
        "status": "shipped"
    },
    1236: {
        "weight": 2.5,
        "content": "clothing",
        "status": "delivered"
    },
    1237: {
        "weight": 0.8,
        "content": "books",
        "status": "placed"
    },
    1238: {
        "weight": 3.1,
        "content": "kitchenware",
        "status": "processing"
    },
    1239: {
        "weight": 1.7,
        "content": "shoes",
        "status": "shipped"
    },
    1240: {
        "weight": 0.4,
        "content": "cosmetics",
        "status": "delivered"
    },
    1241: {
        "weight": 4.2,
        "content": "furniture",
        "status": "processing"
    },
    1242: {
        "weight": 1.0,
        "content": "toys",
        "status": "placed"
    },
    1243: {
        "weight": 2.8,
        "content": "sports equipment",
        "status": "delivered"
    }
}

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str ,Any]:
    latest_id = max(db.keys())
    return db[latest_id]

@app.get("/shipment/{int_id}")
def get_shipment(int_id :int) -> dict[str ,Any]:
    if int_id not in db:
        raise {"details" : f"{int_id} does not exist"}
    return db[int_id]