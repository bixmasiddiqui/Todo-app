"""FastAPI application entry point."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import create_db

app = FastAPI(
    title="Todo API",
    description="RESTful API for Full-Stack Todo Web Application",
    version="1.0.0",
)

# CORS middleware
origins = [origin.strip() for origin in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db()


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "detail": str(exc.detail)},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": "An unexpected error occurred"},
    )


@app.get("/")
async def root():
    return {"message": "Todo API", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Import and include routers
from .routers import tasks

app.include_router(tasks.router)
