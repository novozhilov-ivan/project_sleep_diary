from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field, computed_field


class SleepNote(BaseModel):
    """Запись в дневнике сна"""

    sleep_date: date = Field(
        title="Дата",
        examples=["2021-12-13", "2021-12-14", "2021-12-15", "2021-12-16"],
    )
    went_to_bed: time = Field(
        title="Лег",
        examples=["05:11", "01:55", "01:10", "04:10"],
    )
    fell_asleep: time = Field(
        title="Уснул",
        examples=["05:30", "02:20", "01:30", "04:20"],
    )
    woke_up: time = Field(
        title="Проснулся",
        examples=["12:00", "07:57", "10:00", "11:50"],
    )
    got_up: time = Field(
        title="Встал",
        examples=["12:15", "08:07", "10:30", "12:15"],
    )
    no_sleep: time = Field(
        title="Не спал",
        examples=["00:19", "00:32", "00:06", "01:20"],
    )
    model_config = ConfigDict(from_attributes=True)


class SleepNoteOptional(BaseModel):
    """Запись в дневнике сна. Поля необязательные"""

    sleep_date: date | None = Field(default=None)
    went_to_bed: time | None = Field(default=None)
    fell_asleep: time | None = Field(default=None)
    woke_up: time | None = Field(default=None)
    got_up: time | None = Field(default=None)
    no_sleep: time | None = Field(default=None)
    model_config = ConfigDict(from_attributes=True)


class ListWithSleepNotes(BaseModel):
    notes: list[SleepNote]


class SleepNoteStatistics(SleepNote):
    sleep_duration: time
    time_spent_in_bed: time
    sleep_efficiency: float


class SleepNoteMeta(BaseModel):
    id: int = Field(
        title="Идентификатор записи дневника сна",
    )
    owner_id: int = Field(
        title="Идентификатор владельца дневника сна",
    )


class SleepNoteModel(SleepNoteStatistics, SleepNoteMeta):
    """Запись в дневнике сна со статистикой и идентификаторами пользователя и
    записи."""

    model_config = ConfigDict(from_attributes=True)


class SleepNoteWithMeta(SleepNote, SleepNoteMeta):
    pass


class SleepNoteWithStats(SleepNoteWithMeta):
    @staticmethod
    def time_to_minutes(time_point: time) -> int:
        return time_point.hour * 60 + time_point.minute

    @staticmethod
    def time_diff(subtractor: time, subtrahend: time) -> int:
        diff = SleepNoteWithStats.time_to_minutes(subtractor)
        diff -= SleepNoteWithStats.time_to_minutes(subtrahend)
        return diff

    @staticmethod
    def minutes_to_time(minutes: int) -> time:
        if minutes < 0:
            minutes = 0
        return time(hour=minutes // 60, minute=minutes % 60)

    @computed_field
    @property
    def sleep_duration(self) -> time:
        minutes_of_sleep = self.time_diff(self.woke_up, self.fell_asleep)
        minutes_of_sleep -= self.time_to_minutes(self.no_sleep)
        return self.minutes_to_time(minutes_of_sleep)

    @computed_field
    @property
    def time_spent_in_bed(self) -> time:
        minutes_in_bed = self.time_diff(self.got_up, self.went_to_bed)
        return self.minutes_to_time(minutes_in_bed)

    @computed_field
    @property
    def sleep_efficiency(self) -> float:
        minutes_of_sleep = self.time_to_minutes(self.sleep_duration)
        minutes_in_bed = self.time_to_minutes(self.time_spent_in_bed)
        if minutes_of_sleep == 0:
            return 0
        return round(minutes_of_sleep / minutes_in_bed * 100, 2)