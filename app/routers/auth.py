import os
import uuid
import requests

from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.core.oauth import oauth
from app.core.jwt import create_access_token
from app.core.datetime.functions import utcnow


router = APIRouter()


@router.get("/login")
async def login(request: Request) -> None:
    request.session.clear()
    referer = request.headers.get("referer")
    frontend_url = os.getenv("FRONTEND_URL")
    redirect_url = os.getenv("REDIRECT_URL")
    request.session["login_redirect"] = frontend_url
    return await oauth.google.authorize_redirect(request, redirect_url, prompt="consent")


@router.route("/auth")
async def auth(request: Request) -> RedirectResponse:
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Google authentication failed.") from e

    try:
        user_info_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        google_response = requests.get(user_info_endpoint, headers=headers, timeout=10)
        user_info = google_response.json()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Google authentication failed.") from e

    user = token.get("userinfo")
    expires_in = token.get("expires_in")
    user_id = user.get("sub")
    iss = user.get("iss")
    user_email = user.get("email")
    first_logged_in = utcnow()
    last_accessed = utcnow()

    user_name = user_info.get("name")
    user_pic = user_info.get("picture")

    if iss not in ["https://accounts.google.com", "accounts.google.com"]:
        raise HTTPException(status_code=401, detail="Google authentication failed.")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Google authentication failed.")

    # Create JWT token
    access_token_expires = timedelta(seconds=expires_in)
    access_token = create_access_token(data={"sub": user_id, "email": user_email}, expires_delta=access_token_expires)

    session_id = str(uuid.uuid4())

    redirect_url = request.session.pop("login_redirect", "")
    response = RedirectResponse(redirect_url)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return response
