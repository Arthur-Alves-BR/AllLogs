from app.models.user import User
from app.core.services import BaseService

user_service = BaseService(model=User, default_filters={"is_active": True})
