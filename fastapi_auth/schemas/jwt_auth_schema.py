from pydantic import BaseModel


# Pydantic models for request and response bodies


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str


class ErrorResponse(BaseModel):
    detail: str
