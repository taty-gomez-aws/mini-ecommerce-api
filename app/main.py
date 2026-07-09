from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import products

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-commerce API")

app.include_router(products.router)


@app.get("/")
def read_root():
    return {"status": "ok", "service": "ecommerce-api"}