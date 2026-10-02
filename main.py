import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models  # noqa: F401  (registers tables)
from routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Crop Advisor API", version="1.0.0", lifespan=lifespan)

origins = [o.strip() for o in os.getenv(
    "CORS_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500").split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)

@app.get("/")
def root():
    return {"app": "Crop Advisor API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
