from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from core import settings
from routes import base, data
from stores.llm.providers.LLMProviderFactory import LLMProviderFactory

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():

    app.state.db_connection = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.db_client = app.state.db_connection[settings.MONGODB_DATABASE]
    app.state.llm_provider_factory = LLMProviderFactory(settings)

    app.state.llm_generation_provider = app.state.llm_provider_factory.create_provider(settings.GENERATION_BACKEND)
    app.state.llm_generation_provider.set_generatoin_model(settings.OPENAI_GENERATION_MODEL) # type: ignore

    app.state.llm_embedding_provider = app.state.llm_provider_factory.create_provider(settings.EMBEDDING_BACKEND)
    app.state.llm_embedding_provider.set_embedding_model(settings.COHERE_EMBEDDING_MODEL, settings.EMBEDDING_MODEL_SIZE) # type: ignore


@app.on_event("shutdown")
async def shutdown_db_connection():
    app.state.db_connection.close()


app.include_router(base.base_router)
app.include_router(data.data_router)
