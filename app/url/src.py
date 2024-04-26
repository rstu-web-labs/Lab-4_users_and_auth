import hashlib
import random

from app.models import  add_short_url

def generate_short_link(original_link, session):

    short_link = generate_short_string(original_link)
    add_short_url(original_link, short_link, session)

    return {"url": original_link, "short_url": short_link}
    

def generate_short_string(input_string: str) -> str:
    hash_value = hashlib.sha256(input_string.encode()).hexdigest()
    random_chars = random.sample(hash_value, 8)
    return ''.join(random_chars)