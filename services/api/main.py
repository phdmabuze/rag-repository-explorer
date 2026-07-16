from fastapi import APIRouter, FastAPI

from .routes import router

app = FastAPI(
    title="RAG Repository Explorer",
)

root_router = APIRouter(prefix="/api/v1")

root_router.include_router(router)

app.include_router(root_router)
