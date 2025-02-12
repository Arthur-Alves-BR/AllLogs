from pydantic import UUID4
from datetime import datetime, UTC
from typing import Any, TypeVar, Generic

from tortoise.models import Model
from tortoise.queryset import QuerySet
from tortoise.exceptions import DoesNotExist

from fastapi import HTTPException, status


T = TypeVar("T", bound=Model)


class BaseService(Generic[T]):
    def __init__(self, model: type[T], default_filters: dict[str, Any] | None = None) -> None:
        """Initializes the service with the model and optional default filters."""
        self.model = model
        self._default_filters = default_filters if default_filters else {}

    @property
    def _base_query(self) -> QuerySet[T]:
        """Returns the base query with default filters applied."""
        return self.model.filter(**self._default_filters)

    async def get_all(self) -> list[T]:
        """Retrieve all records of the model."""
        return await self._base_query.all()

    async def get_by_id(self, id: UUID4) -> T:
        """Retrieves a single record by its id.

        Raises a 404 HTTP exception if the record is not found.
        """
        try:
            instance = await self._base_query.get(id=id)
        except DoesNotExist as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found") from e
        return instance

    async def create(self, data: dict) -> T:
        """Create a new record using the provided data."""
        return await self.model.create(**data)

    async def update(self, id: UUID4, data: dict) -> T:
        """Update an existing record by its id with the provided data."""
        instance = await self.get_by_id(id)
        await instance.update_from_dict(data)
        await instance.save()
        return instance

    async def delete(self, id: UUID4) -> None:
        """Deletes a record by its id."""
        instance = await self.get_by_id(id)
        await instance.delete()

    async def soft_delete(self, id: UUID4) -> None:
        """Soft delete a record by setting 'is_active' to False."""
        instance = await self.get_by_id(id)
        instance.is_active = False
        instance.deleted_at = datetime.now(UTC)
        await instance.save()
