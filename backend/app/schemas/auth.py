from pydantic import BaseModel


class LoginData(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenUser(BaseModel):
    id: str
    name: str
    email: str
    company_id: str


class RefreshTokenUser(BaseModel):
    id: str
