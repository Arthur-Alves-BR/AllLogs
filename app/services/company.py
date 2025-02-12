from app.models.company import Company
from app.core.services import BaseService

company_service = BaseService(model=Company, default_filters={"is_active": True})
