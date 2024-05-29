from pydantic import BaseModel
from typing import Optional

class UrlIn(BaseModel):
    url: str
    short_url: str = None

class UrlOut(BaseModel):
    short_url: str
    url: str
    created_at: str
    share_url: Optional[str] = None

