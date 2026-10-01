import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.session import engine, Base
from app.api.cases import router as cases_router
from app.api.documents import router as documents_router
from app.api.approvals import router as approvals_router
from app.api.counterfactual import router as counterfactual_router
from app.api.integrations import router as integrations_router
from app.api.insights import router as insights_router
from app.api.health import router as health_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bharatresolve.main")

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="BharatResolve AI - Agentic AI Case-Resolution Engine for India"
)

# Enable CORS with configurable origins
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(cases_router)
app.include_router(documents_router)
app.include_router(approvals_router)
app.include_router(counterfactual_router)
app.include_router(integrations_router)
app.include_router(insights_router)
app.include_router(health_router)

@app.on_event("startup")
def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} on port {settings.PORT}...")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    logger.info(f"LLM Model: {settings.GEMINI_MODEL} (Ollama Fallback: {settings.OLLAMA_BASE_URL})")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
