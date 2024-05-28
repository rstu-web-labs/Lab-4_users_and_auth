from fastapi import FastAPI
from app.endpoints.endp import router
from app.core.db import engine
from app.core.init_db import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)