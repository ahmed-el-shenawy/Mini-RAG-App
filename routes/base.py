from fastapi import APIRouter,FastAPI
import os

base_router = APIRouter(
	prefix="/api/v1",
	tags=["Base"],
)

@base_router.get("/")
async def wellcom():
	app_name = os.getenv("APP_NAME", "Mini RAG App")
	app_version = os.getenv("APP_VERSION", "0.1.0")
	return {
		"message":"Welcome to Mini RAG App!",
		"app_name": app_name,
		"app_version": app_version
		}
