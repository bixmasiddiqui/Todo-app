"""FastAPI application entry point."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings

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


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 Not Found errors."""
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "detail": str(exc.detail)},
    )


@app.exception_handler(422)
async def validation_error_handler(request: Request, exc: HTTPException):
    """Handle 422 Validation errors."""
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "detail": str(exc.detail)},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 Internal Server errors."""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": "An unexpected error occurred"},
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Todo API", "docs": "/docs"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Import and include routers
from .routers import tasks

app.include_router(tasks.router)
