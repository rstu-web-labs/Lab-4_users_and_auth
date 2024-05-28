from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import reset_loggers,logger
from app.core.settings import app_settings
from app.metrics import router as router_metrics

# from app.models import create_database, delete_tables
from app.short import router as router_short
from app.users import router as router_user

# from prometheus_client import make_asgi_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    reset_loggers()
    logger.info("Приложение запущено")
    yield
    logger.info("Выключение")


app = FastAPI(title="Укротитель Урлов", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)

# metrics_app = make_asgi_app()
# app.mount("/metrics", metrics_app)

app.include_router(router_short)
app.include_router(router_user)
app.include_router(router_metrics)

if not app_settings.local:
    reset_loggers()
