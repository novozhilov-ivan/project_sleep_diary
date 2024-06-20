from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from src.extension import db
from src.models import UserOrm


def read_user_by_username(username: str) -> UserOrm | None:
    """Получает пользователя по username"""
    db_response = db.session.execute(
        select(
            UserOrm,
        ).where(
            UserOrm.username == username,
        )
    )
    return db_response.scalar_one_or_none()


def find_user_by_id(user_id: int) -> UserOrm | None:
    """Получает пользователя по id"""
    db_response = db.session.execute(
        select(
            UserOrm,
        ).where(
            UserOrm.id == user_id,
        )
    )
    return db_response.scalar_one_or_none()


def delete_user_by_id(user_id: int) -> None:
    """Удалить пользователя"""
    db.session.execute(
        delete(
            UserOrm,
        ).where(
            UserOrm.id == user_id,
        )
    )


def create_new_user_by_username(user: UserOrm) -> UserOrm | None:
    """Создать нового пользователя"""
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        return None
    else:
        db.session.refresh(user)
        return user