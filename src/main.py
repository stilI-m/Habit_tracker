from fastapi import FastAPI

from src.config import get_settings

settings = get_settings()

app = FastAPI(title= settings.project_name)

@app.get("/ping")
async def ping():
    return {"status": "OK", "project": settings.project_name}

