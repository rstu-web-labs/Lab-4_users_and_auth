import hashlib
import base64
import hmac


def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False

    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)

    if not (has_lower and has_upper and has_digit):
        return False

    return True

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_verification_token(email: str, secret_key: str) -> str:
    email_baseencode = base64.b64encode(email.encode()).decode()
    signature = hmac.new(secret_key.encode(), email_baseencode.encode(), hashlib.sha256).hexdigest()
    return f"{email_baseencode}-{signature}"

def verify_token_signature(email_baseencode: str, signature: str, secret_key: str) -> bool:
    expected_signature = hmac.new(secret_key.encode(), email_baseencode.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)
