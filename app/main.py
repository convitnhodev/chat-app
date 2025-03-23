from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers.base import api_router

def include_router(app):
    app.include_router(api_router)

def start_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION
    )
    origins = ["http://localhost:5173"]  # Replace with the origin(s) of your frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_router(app)
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
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=True    # Add reload for development
    )