from tortoise import fields

from app.core.models import SoftDeleteModel, TimestampedModel


class Company(SoftDeleteModel, TimestampedModel):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=100)

    class Meta:
        table = "companies"
