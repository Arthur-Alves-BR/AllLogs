from fastapi import Request

from app.schemas.auth import TokenUser


class AppRequest(Request):
    """Custom request class for the application, with user typing."""

    @property
    def user(self) -> TokenUser | None:
        return self.state.user
