from tortoise import fields

from app.core.models import SoftDeleteModel, TimestampedModel


class Application(SoftDeleteModel, TimestampedModel):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    company = fields.ForeignKeyField(
        "models.Company",
        related_name="applications",
        on_delete=fields.CASCADE,
        null=False,
    )

    class Meta:
        table = "applications"
