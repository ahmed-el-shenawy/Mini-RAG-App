from fastapi import APIRouter
from core.config import settings

base_router = APIRouter(
	prefix="/api/v1",
	tags=["Base"],
)

@base_router.get("/")
async def wellcom():
	return {
		"message":"Welcome to Mini RAG App!",
		"app_name": settings.APP_NAME,
		"app_version": settings.APP_VERSION
		}
