
from typing import Dict
from fastapi import FastAPI, HTTPException, Request, status

app = FastAPI()

#AI
database: Dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Laptop Pro 15",
        "price": 45000000.0,
        "stock": 12,
        "category": "Electronics"
    },
    2: {
        "id": 2,
        "name": "Mechanical Keyboard",
        "price": 3200000.0,
        "stock": 35,
        "category": "Accessories"
    },
    3: {
        "id": 3,
        "name": "Wireless Headphones",
        "price": 5800000.0,
        "stock": 20,
        "category": "Audio"
    },
}


def extract_trace_context(request: Request) -> dict:
    return {
        "traceparent": request.headers.get("traceparent"),
        "x_request_id": request.headers.get("x-request-id"),
        "consumer": request.headers.get("x-consumer-username", "anonymous"),
    }


@app.get("/api/products", status_code=status.HTTP_200_OK)
async def list_products(request: Request):

    return {
        "service": "products-service",
        "trace": extract_trace_context(request),
        "count": len(database),
        "data": list(database.values()),
    }


@app.get("/api/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: int, request: Request):

    if product_id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return {
        "service": "products-service",
        "trace": extract_trace_context(request),
        "data": database[product_id],
    }
