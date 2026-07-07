from fastapi import FastAPI

app = FastAPI(title="Mini E-commerce API")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "ecommerce-api"}