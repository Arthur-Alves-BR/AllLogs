from app.models import Application
from app.core.services import BaseService

application_service = BaseService(model=Application, default_filters={"is_active": True})
