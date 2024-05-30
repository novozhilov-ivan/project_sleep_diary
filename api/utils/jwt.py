import uuid
from datetime import datetime, timedelta
from functools import wraps
from typing import Literal

import jwt
from flask import request
from flask_restx import abort
from jwt import InvalidTokenError

from api import config
from api.extension import bearer
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserValidate

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

response_invalid_authorization_token_401 = "invalid authorization token"
response_invalid_token_type_401 = "invalid token type {} expected {}"


def encode_jwt(
    payload: dict,
    private_key: str = config.auth_jwt.private_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    utc_now = datetime.utcnow()
    if expire_timedelta:
        expire = utc_now + expire_timedelta
    else:
        expire = utc_now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=utc_now, jti=str(uuid.uuid4()))
    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = config.auth_jwt.public_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
) -> dict:
    try:
        return jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
    except InvalidTokenError:
        abort(
            code=HTTP.UNAUTHORIZED_401,
            message=response_invalid_authorization_token_401,
        )


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_jwt(user: UserValidate) -> str:
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=config.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_jwt(user: UserValidate) -> str:
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(
            days=config.auth_jwt.refresh_token_expire_days,
        ),
    )


def validate_token_type(
    payload: dict,
    token_type: str | Literal["access", "refresh"],
) -> None:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        abort(
            code=HTTP.UNAUTHORIZED_401,
            message=response_invalid_token_type_401.format(
                f"{current_token_type!r}",
                f"{token_type!r}",
            ),
        )


def validate_auth_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header: str | None = request.headers.get("Authorization")

        if auth_header is None or bearer not in auth_header:
            abort(
                code=HTTP.UNAUTHORIZED_401,
                message=response_invalid_authorization_token_401,
            )
        *_, token = auth_header.split(" ")
        decode_jwt(token=token)
        return f(*args, **kwargs)

    return decorated


def get_current_token_payload() -> dict:
    credentials = request.headers.get("Authorization")
    *_, token = credentials.split(" ")
    return decode_jwt(token=token)
