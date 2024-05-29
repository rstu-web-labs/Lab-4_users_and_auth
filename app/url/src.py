import hashlib
import random

from app.models import  add_short_url, add_short_url_auth, get_short_url

def generate_short_link(original_link, user, session):
    if user:
        short_link = get_short_url(original_link, session)
        if not short_link or not short_link.user_id:
            short_url = generate_short_string(original_link)
            user_id = add_short_url_auth(original_link, short_url, user, session)
        else:
            short_url = short_link.short_url
            user_id = short_link.user_id
        return {
            "url": original_link, 
            "short_url": short_url,
            "share_url": f'http://localhost/api/url/{short_url}?u={user_id}'
        }
    else:
        short_link = get_short_url(original_link, session)
        if not short_link:
            short_url = generate_short_string(original_link)
            add_short_url(original_link, short_url, session)
        else:
            short_url = short_link.short_url
    return {
        "url": original_link, 
        "short_url": short_url,
        "share_url": f'http://localhost/api/url/{short_url}'
    }
    

def generate_short_string(input_string: str) -> str:
    hash_value = hashlib.sha256(input_string.encode()).hexdigest()
    random_chars = random.sample(hash_value, 8)
    return ''.join(random_chars)