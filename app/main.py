from fastapi import FastAPI
from .routers import health

app = FastAPI(title="NOVEYA • AI Health Module", version="0.1.0")
app.include_router(health.router, prefix="/v1", tags=["health"])

@app.get("/", tags=["meta"])
def root():
    return {
        "name": "NOVEYA • AI Health Module",
        "status": "ok"
    }
