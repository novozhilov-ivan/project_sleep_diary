from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from src import repository
from src.domain.note import NoteEntity, NoteTimePoints
from src.orm import NoteORM, UserORM


def test_repo_can_add_and_save_note(
    session: Session,
    create_user: UserORM,
) -> None:
    note_time_points = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    repo = repository.SQLAlchemyDiaryRepository(
        session=session,
        owner_id=create_user.oid,
    )
    repo.add(note_time_points)
    session.commit()

    [result] = session.execute(
        text(
            "SELECT bedtime_date, went_to_bed, fell_asleep, woke_up, got_up "
            'FROM "notes";',
        ),
    )
    assert result == (
        "2020-12-12",
        "13:00:00.000000",
        "15:00:00.000000",
        "23:00:00.000000",
        "01:00:00.000000",
    )


def insert_note(session: Session, user: UserORM) -> NoteORM:
    note_time_points = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    note_orm = NoteORM.from_time_points(
        obj=note_time_points,
        owner_id=user.oid,
    )
    session.add(note_orm)
    session.commit()
    session.refresh(note_orm)
    return note_orm


def test_repo_can_retrieve_note_by_oid(
    session: Session,
    create_user: UserORM,
) -> None:
    inserted_note_orm = insert_note(session, create_user)

    repo = repository.SQLAlchemyDiaryRepository(
        session=session,
        owner_id=create_user.oid,
    )
    retrieved = repo.get(oid=inserted_note_orm.oid)

    assert isinstance(retrieved, NoteEntity)
    assert isinstance(retrieved.oid, UUID)
    assert isinstance(retrieved.created_at, datetime)
    assert isinstance(retrieved.updated_at, datetime)
    assert retrieved.bedtime_date == date(2020, 12, 12)
    assert retrieved.went_to_bed == time(13, 0)
    assert retrieved.fell_asleep == time(15, 0)
    assert retrieved.woke_up == time(23, 0)
    assert retrieved.got_up == time(1, 0)
    assert retrieved.no_sleep == time(0, 0)


def test_repo_can_retrieve_note_by_bedtime_date(
    session: Session,
    create_user: UserORM,
) -> None: ...


def test_repo_can_retrieve_diary(
    session: Session,
    create_user: UserORM,
) -> None: ...
