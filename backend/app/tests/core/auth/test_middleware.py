import pytest

from unittest.mock import AsyncMock

from fastapi import Request

from app.core.auth.user import create_user_token
from app.core.auth.middleware import UserMiddleware


@pytest.fixture
def middleware():
    return UserMiddleware(app=None)


@pytest.fixture
def mock_request():
    request = AsyncMock(Request)
    request.scope = {}
    return request


async def test_dispatch_without_token(middleware, mock_request):
    """Test middleware with no token in the header."""
    mock_request.headers.get.return_value = None  # No auth
    await middleware.dispatch(mock_request, AsyncMock())
    assert mock_request.scope["user"] is None


async def test_dispatch_with_invalid_token(middleware, mock_request):
    """Test middleware with an incorrectly formatted token."""
    mock_request.headers.get.return_value = "InvalidTokenFormat"
    await middleware.dispatch(mock_request, AsyncMock())
    assert mock_request.scope["user"] is None


async def test_dispatch_with_valid_token(middleware, mock_request, test_user):
    """Test middleware with a valid token."""
    mock_request.headers.get.return_value = f"Bearer {create_user_token(test_user).access_token}"
    await middleware.dispatch(mock_request, AsyncMock())
    assert mock_request.scope["user"].id == str(test_user.id)
