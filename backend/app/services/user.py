from app.models import User
from app.core.services import BaseService

from app.core.auth.password import hash_password


class UserService(BaseService):
    model = User
    default_filters = {"is_active": True}

    def create(self, data: dict) -> User:
        data["password"] = hash_password(data["password"])
        return super().create(data)
