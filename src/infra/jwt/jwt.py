from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing_extensions import Self
from uuid import uuid4

from jwt import DecodeError, PyJWTError, decode, encode

from src.infra.jwt.base import IJWTService, IPayload, JWTType
from src.infra.jwt.exceptions import DecodeJWTException, EncodeJWTException
from src.project.settings import AuthJWTSettings


@dataclass(kw_only=True)
class JWTPayload(IPayload):
    typ: JWTType
    iat: int = field(default_factory=lambda: int(datetime.now(UTC).timestamp()))
    exp: int
    jti: str = field(default_factory=lambda: str(uuid4()))

    external_payload: IPayload | None = None

    def convert_to_dict(self: Self) -> dict:
        jwt_payload = {
            "typ": self.typ,
            "iat": self.iat,
            "exp": self.exp,
            "jti": self.jti,
        }
        if self.external_payload:
            jwt_payload.update(self.external_payload.convert_to_dict())

        return jwt_payload


@dataclass
class JWTService(IJWTService):
    settings: AuthJWTSettings

    def encode(self: Self, payload: dict) -> str:
        try:
            return encode(
                payload=payload,
                key=self.settings.private_key,
                algorithm=self.settings.algorithm,
            )
        except PyJWTError:
            raise EncodeJWTException

    def decode(self: Self, jwt: str) -> dict:
        try:
            return decode(
                jwt=jwt,
                key=self.settings.public_key,
                algorithms=[self.settings.algorithm],
            )
        except DecodeError:
            raise DecodeJWTException

    def create_jwt(
        self: Self,
        jwt_type: JWTType,
        payload: IPayload | None = None,
        expire: int = 0,
    ) -> str:
        return self.encode(
            payload=JWTPayload(
                typ=jwt_type,
                exp=self.get_expired_at(jwt_type, expire),
                external_payload=payload,
            ).convert_to_dict(),
        )

    def get_jwt_payload(self: Self, jwt: str) -> dict:
        return self.decode(jwt)

    def get_expired_at(
        self: Self,
        token_type: JWTType,
        expire: int = 0,
    ) -> int:
        if expire:
            return int(datetime.now(UTC).timestamp() + expire)

        default_expire_by_token_type: int

        if token_type == JWTType.ACCESS:
            default_expire_by_token_type = self.settings.access_token_expire
        else:
            default_expire_by_token_type = self.settings.refresh_token_expire

        return int(datetime.now(UTC).timestamp() + default_expire_by_token_type)
