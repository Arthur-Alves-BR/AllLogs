import re
import bcrypt


MIN_PASSWORD_LENGTH = 8


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=plain_password.encode("utf-8"), hashed_password=hashed_password.encode("utf-8"))


def is_valid_password(password: str) -> str:
    error_messages = []

    if len(password) < MIN_PASSWORD_LENGTH:
        error_messages.append("The password is too short")

    if not re.search(r"[A-Z]", password):
        error_messages.append("The password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        error_messages.append("The password must contain at least one lowercase letter")

    if not re.search(r"[0-9]", password):
        error_messages.append("The password must contain at least one digit")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        error_messages.append("The password must contain at least one special character")

    if error_messages:
        raise ValueError(error_messages)

    return password
