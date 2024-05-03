from fastapi import APIRouter

from app.api.endpoints import rout, reg_router, auth_router, verif_router

router = APIRouter()

router.include_router(rout,  prefix='/api/url')
router.include_router(reg_router,  prefix='/api', tags=['Регистрация'])
router.include_router(auth_router, prefix='/api', tags=['Авторизация'])
router.include_router(verif_router,  prefix='/api', tags=['Подтверждение почты'])
