from tortoise import fields
from tortoise.models import Model


class SoftDeleteModel(Model):
    is_active = fields.BooleanField(default=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        abstract = True
