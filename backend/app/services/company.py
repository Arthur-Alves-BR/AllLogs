from app.models import Company
from app.core.services import BaseService


class CompanyService(BaseService):
    model = Company
    default_filters = {"is_active": True}
