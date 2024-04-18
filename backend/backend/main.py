# Load environment variables first
from load_env import load_env

load_env()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generation import generate_code

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(generate_code.router)
