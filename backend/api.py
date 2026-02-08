"""Vercel serverless entry point for the FastAPI backend."""

from src.main import app

# Vercel's @vercel/python runtime detects the `app` variable
# and wraps the ASGI application for serverless execution.

# Local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
