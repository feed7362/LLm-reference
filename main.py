from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm_manager import LLMEngine
from websocket import websocket_router
from prompts import validate_metadata
from contextlib import asynccontextmanager

from utils.logger import CustomLogger
logger = CustomLogger(__name__)

def initialize_engine() -> LLMEngine:
    engine = LLMEngine()
    engine.warmup()
    logger.info("Engine warmup complete")
    return engine

def cleanup_engine(engine: LLMEngine) -> None:
    engine.close()
    logger.info("Engine closed")

def validate_application_metadata() -> None:
    validate_metadata()
    logger.info("Metadata validation complete")


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = None
    try:
        logger.info("Lifespan: start")
        engine = initialize_engine()
        validate_application_metadata()
        yield
    except Exception as e:
        logger.exception(f"Lifespan error: {str(e)}")
        raise
    finally:
        if engine:
            cleanup_engine(engine)

model_app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:2222",
    "http://127.0.0.1:2222",
]

model_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
model_app.include_router(websocket_router)