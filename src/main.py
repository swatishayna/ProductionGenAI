import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn


@asynccontextmanager
def lifespan(app: FastAPI):
    """asynccontextmanager is a decorator from Python's contextlib module 
    that converts an async generator function into an asynchronous 
    context manager. Code before yield is executed when entering the context 
    (setup/startup), and code after yield is executed when exiting the context 
    (cleanup/shutdown). FastAPI uses it in the lifespan function to initialize
    shared resources such as databases, vector stores, 
    and LLM clients during startup and release them during application shutdown."""
    
    print("Start")
    yield "Do Something"
    print("Cleanup")
    
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
