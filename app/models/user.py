from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=100)
