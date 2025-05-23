import uvicorn
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.crud import fetch_data
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    fetch_data(1000)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
