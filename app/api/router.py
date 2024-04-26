from fastapi import APIRouter

from app.api.endpoints import rout, reg_router

main_router = APIRouter()

main_router.include_router(rout,  prefix='/api/url')
main_router.include_router(reg_router,  prefix='/api', tags=['Регистрация'])

