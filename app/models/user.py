from tortoise import fields

from app.core.models import SoftDeleteModel, TimestampedModel


class User(SoftDeleteModel, TimestampedModel):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, unique=True)
    company = fields.ForeignKeyField("models.Company", related_name="users", on_delete=fields.CASCADE, null=False)

    class Meta:
        table = "users"
