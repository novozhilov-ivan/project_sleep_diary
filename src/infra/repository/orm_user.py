from dataclasses import dataclass
from typing_extensions import Self

from sqlalchemy import select

from src.domain.entities import UserEntity
from src.domain.services import IUsersRepository
from src.infra.database import Database
from src.infra.orm import ORMUser


@dataclass
class ORMUsersRepository(IUsersRepository):
    database: Database

    def get_by_username(self: Self, username: str) -> UserEntity | None:
        stmt = select(ORMUser).where(ORMUser.username == username).limit(1)

        with self.database.get_session() as session:
            result = session.scalar(stmt)

        if isinstance(result, ORMUser):
            return result.to_entity()
        return None

    def add_user(self: Self, user: UserEntity) -> None: ...

    def delete_user(self: Self, username: str) -> None: ...
