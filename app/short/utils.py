from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import CustomUrlBase, OriginalUrlBase
from app.short.crud import get_short_url_in, get_short_url_in_all, set_original_url
from app.short.RandomLink import RandomLink


def generate_response_url(data: OriginalUrlBase, db: Session, user_id: str | None = None):
    data_custom = CustomUrlBase(url=str(data.url))
    if data.short_url:
        data_custom.custom_url = data.short_url
        if user_id:
            data_custom.share_url = f"http://0.0.0.0:8005/api/url/{data_custom.custom_url}?u={user_id}"
        else:
            data_custom.share_url = f"http://0.0.0.0:8005/api/url/{data_custom.custom_url}"
        if get_short_url_in(db, data.short_url):
            raise HTTPException(
                status_code=418,
                detail="Придумайте другую короткую сслыку или оставьте поле пустым",
                headers={"X-Error": "There goes my error"},
            )
        elif user_id:
            set_original_url(db, data, user_id)
        else:
            set_original_url(db, data)
    else:
        generate_urls = get_short_url_in_all(db, RandomLink.array_random_links())
        if len(generate_urls) > 0:
            data.short_url = generate_urls[0]
            data_custom.custom_url = data.short_url
            if user_id:
                data_custom.share_url = f"http://0.0.0.0:8005/api/url/{data_custom.custom_url}?u={user_id}"
                set_original_url(db, data, user_id)
            else:
                data_custom.share_url = f"http://0.0.0.0:8005/api/url/{data_custom.custom_url}"
                set_original_url(db, data)
    return data_custom
