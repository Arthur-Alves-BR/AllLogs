from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.auth.user import get_current_user


class UserMiddleware(BaseHTTPMiddleware):
    """Middleware that adds the authenticated user to the request scope."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        token = request.headers.get("Authorization")
        if token and "Bearer " not in token:
            token = None

        user = get_current_user(token.split()[1]) if token else None
        request.scope.update({"user": user})

        return await call_next(request)
