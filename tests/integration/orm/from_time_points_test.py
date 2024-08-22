from sqlalchemy.orm import Session

from src.domain.note import NoteTimePoints
from src.orm.note import ORMNote
from src.orm.user import ORMUser


def test_note_orm_from_time_points(
    session: Session,
    create_user: ORMUser,
) -> None:
    note_time_points = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    note_orm = ORMNote.from_time_points(
        obj=note_time_points,
        owner_id=create_user.oid,
    )
    session.add(note_orm)
    session.commit()
    session.refresh(note_orm)

    assert note_orm.oid
    assert note_orm.created_at
    assert note_orm.updated_at
    assert note_orm.bedtime_date == note_time_points.bedtime_date
    assert note_orm.went_to_bed == note_time_points.went_to_bed
    assert note_orm.fell_asleep == note_time_points.fell_asleep
    assert note_orm.woke_up == note_time_points.woke_up
    assert note_orm.got_up == note_time_points.got_up
