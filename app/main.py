from fastapi import FastAPI
from app.core.config import settings

def start_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION
    )
    return app

app = start_application()

@app.get('/', tags=["Root"])
def hello_api():
    """
    Root endpoint that returns a welcome message
    """
    return {
        "message": "Welcome to FastAPI",
        "project_name": settings.PROJECT_TITLE
    }

@app.get('/health', tags=["Health"])
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)