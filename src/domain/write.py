from src.domain import diary as dr, note as nt
from src.domain.errors import NoteAlreadyExist


def write(note: nt.NoteValueObject, diary: dr.Diary) -> nt.NoteStatistic:
    if diary.can_write(note):
        diary.write(note)
        return nt.NoteStatistic.model_validate(note, from_attributes=True)
    raise NoteAlreadyExist(
        f"Запись о сне с датой {note.bedtime_date} уже существует в дневнике.",
    )