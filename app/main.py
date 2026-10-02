from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from app.database.connection import init_db
from app.routes.tasks import router as tasks_router
from app.routes.auth import router as auth_router
from app.routes.public import router as public_router
from app.routes.protected import router as protected_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed initial data if empty
    init_db()
    yield

app = FastAPI(
    title="Todo API",
    description="A lightweight RESTful API for managing tasks with clean layered architecture, PostgreSQL, and Docker Compose.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(public_router)
app.include_router(protected_router)
