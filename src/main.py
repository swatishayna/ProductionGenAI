import os
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
import uvicorn

#setup logging
logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s  - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """asynccontextmanager is a decorator from Python's contextlib module 
    that converts an async generator function into an asynchronous 
    context manager. Code before yield is executed when entering the context 
    (setup/startup), and code after yield is executed when exiting the context 
    (cleanup/shutdown). FastAPI uses it in the lifespan function to initialize
    shared resources such as databases, vector stores, 
    and LLM clients during startup and release them during application shutdown."""
    
    logger.info("Starting RAG API")
    
    print("Start")
    
    logger.infor("API System Ready")
    yield 
    
    print("Cleanup")
    logger.info("API shutdown complete")
    
    
app = FastAPI(
    title = "Research Paper Curator System",
    description="Production RAG for Research Paper",
    version=os.getenv("APP_VERSION", "0.1.0"),
    root_path = "/api/v1",
    lifespan = lifespan,
)
# The lifespan parameter in FastAPI is used to run code when your application:
# Starts up 🚀
# Shuts down 🛑

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host = "0.0.0.0")
