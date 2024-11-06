from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import Self

from src.domain.entities import UserEntity
from src.service_layer.entities import (
    AccessToken,
    IPayload,
    RefreshToken,
    TokenType,
    UserJWTPayload,
)
from src.service_layer.exceptions import NotAuthenticatedException


@dataclass
class NotAuthenticated:
    def __bool__(self: Self) -> bool:
        return False

    def __repr__(self: Self) -> str:
        return "<NotAuthenticated>"


@dataclass
class IUserAuthenticationService(ABC):
    _user: UserEntity | NotAuthenticated = field(
        default_factory=NotAuthenticated,
        init=False,
    )

    @property
    def user(self: Self) -> UserEntity:
        if isinstance(self._user, NotAuthenticated):
            raise NotAuthenticatedException
        return self._user

    @abstractmethod
    def login(self: Self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def logout(self: Self) -> None:
        raise NotImplementedError

    @abstractmethod
    def register(self: Self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister(self: Self) -> None:
        raise NotImplementedError


@dataclass
class IJWTService(ABC):

    @abstractmethod
    def encode(self: Self, payload: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self: Self, jwt: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_jwt(
        self: Self,
        jwt_type: TokenType,
        payload: IPayload | None = None,
        expire: int = 0,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_jwt_payload(self: Self, jwt: str) -> dict:
        raise NotImplementedError


@dataclass
class IUserJWTAuthorizationService(ABC):

    @abstractmethod
    def create_access(self: Self, user: UserEntity) -> AccessToken:
        raise NotImplementedError

    @abstractmethod
    def create_refresh(self: Self, user: UserEntity) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    def get_payload(self: Self, token: str) -> UserJWTPayload:
        raise NotImplementedError

    @abstractmethod
    def validate_token_type(self: Self, jwt_type: TokenType) -> None:
        raise NotImplementedError

    @abstractmethod
    def deauthorize(self: Self) -> None:
        raise NotImplementedError
