from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

ws_test_router = APIRouter()

# Get the directory where templates are stored
templates_dir = Path(__file__).parent.parent / "static"
templates = Jinja2Templates(directory=str(templates_dir))

@ws_test_router.get("/ws-test", response_class=HTMLResponse)
async def get_ws_test_page(request: Request):
    return templates.TemplateResponse(
        "websocket_test.html",
        {"request": request}
    )