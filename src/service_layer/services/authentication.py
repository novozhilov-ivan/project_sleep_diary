from dataclasses import dataclass
from typing import ClassVar, cast
from typing_extensions import Self

from bcrypt import checkpw, gensalt, hashpw

from src.domain.entities import UserEntity
from src.infra.repository import IUsersRepository
from src.service_layer.exceptions.login import LogInException
from src.service_layer.services.base import IUserAuthenticationService


@dataclass
class UserAuthenticationService(IUserAuthenticationService):
    DEFAULT_ENCODING: ClassVar[str] = "utf-8"
    INVALID_CREDENTIALS_MESSAGE: ClassVar[str] = (
        "Неверное имя пользователя или пароль."
    )

    repository: IUsersRepository

    def login(self: Self, username: str, password: str) -> None:
        self._validate_user(username)
        self._validate_user_password(password)

    @staticmethod
    def _hash_password(pwd_bytes: bytes, decode_from: str = DEFAULT_ENCODING) -> str:
        return hashpw(pwd_bytes, gensalt()).decode(decode_from)

    @staticmethod
    def _compare_passwords(password: bytes, hashed_password: bytes) -> bool:
        return checkpw(password=password, hashed_password=hashed_password)

    def _get_user(self: Self, username: str) -> UserEntity | None:
        return self.repository.get_by_username(username)

    def _validate_user(self: Self, username: str) -> None:
        user: UserEntity | None = self._get_user(username)

        if user is None:
            raise LogInException(self.INVALID_CREDENTIALS_MESSAGE)

        self._user = user
        cast(UserEntity, self._user)

    def _validate_user_password(self: Self, password: str) -> None:
        if not self._compare_passwords(
            password=password.encode(self.DEFAULT_ENCODING),
            hashed_password=self._user.password,
        ):
            raise LogInException(self.INVALID_CREDENTIALS_MESSAGE)