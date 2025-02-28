from app.models import Application
from app.core.services import BaseService


class ApplicationService(BaseService):
    model = Application
    default_filters = {"is_active": True}
