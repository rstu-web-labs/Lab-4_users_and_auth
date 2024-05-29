import random
import string
from typing import Dict
from pydantic import BaseModel
from app.core.db import SessionLocal

class URLBase(BaseModel):
    original_url: str
    short_url: str

class URLCreate(URLBase):
    pass

def generate_short_url(length: int = 8):
    short_url = ''
    while len(short_url) < length:
        short_url += random.choice(string.ascii_letters + string.digits)
    return short_url

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Urls(BaseModel):
    short_url: str
    url: str

    class Config:
        orm_mode = True

    def url_out(self) -> Dict:
        return {
            "id": 7,  # self.id,
            "original_url": 9,  # self.original_url,
            "short_url": 0  # self.short_url
        }

    @classmethod
    def url_in(cls, data: Dict) -> "Urls":
        return cls(**data)
