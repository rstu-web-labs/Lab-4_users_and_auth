import base64
import hashlib

from app.core.settings import app_settings


def hash_pswd(pswd: str, secret_key=app_settings.secret_key) -> str:
    hash = hashlib.sha256()
    hash.update(pswd.encode("utf-8") + secret_key.encode("utf-8"))
    return hash.hexdigest()


def confirm_token_encrypt(email: str, secret_key=app_settings.secret_key) -> str:
    email_encode = base64.b64encode(email.encode("utf-8")).decode("utf-8")
    email_sha256 = hashlib.sha256(email_encode.encode("utf-8") + secret_key.encode("utf-8")).hexdigest()
    return f"{email_encode}-{email_sha256}"


def confirm_token_decrypt(signature: str):
    email_signature = signature.split("-")
    decoded_email = base64.b64decode(email_signature[0]).decode("utf-8")
    original_signature = confirm_token_encrypt(decoded_email)
    if original_signature == signature:
        return decoded_email
    else:
        return False
