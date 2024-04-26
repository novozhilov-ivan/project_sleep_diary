from datetime import time
from typing_extensions import Annotated

from pydantic import BaseModel, computed_field, Field, ConfigDict

from common.pydantic_schemas.sleep.notes import SleepNoteModel, SleepNoteCompute


class SleepDiaryWeeklyStatistic(BaseModel):
    days_count: int
    average_sleep_duration: time
    average_time_spent_in_bed: time
    average_sleep_efficiency: float


class SleepDiaryWeeklyNotesModel(BaseModel):
    notes: list[SleepNoteModel]


class SleepDiaryWeekModel(SleepDiaryWeeklyNotesModel, SleepDiaryWeeklyStatistic):
    model_config = ConfigDict(from_attributes=True)


class SleepDiaryWeeklyNotes(BaseModel):
    notes: Annotated[list[SleepNoteCompute], Field(max_length=7)]


class SleepDiaryWeekCompute(SleepDiaryWeeklyNotes):
    @computed_field
    @property
    def days_count(self) -> int:
        return len(self.notes)

    @staticmethod
    def get_average_time(notes: list[SleepNoteCompute], field_name: str) -> time:
        if not notes:
            return time(0, 0)
        minutes_of_sleep = 0
        for note in notes:
            minutes_of_sleep += note.__getattr__(field_name).hour * 60
            minutes_of_sleep += note.__getattr__(field_name).minute
        average_minutes = minutes_of_sleep // len(notes)
        return time(
            hour=average_minutes // 60,
            minute=average_minutes % 60
        )

    @computed_field
    @property
    def average_sleep_duration(self) -> time:
        return self.get_average_time(notes=self.notes, field_name='sleep_duration')

    @computed_field
    @property
    def average_time_spent_in_bed(self) -> time:
        return self.get_average_time(notes=self.notes, field_name='time_spent_in_bed')

    @computed_field
    @property
    def average_sleep_efficiency(self) -> float:
        sleep_duration = self.average_sleep_duration.hour * 60 + self.average_sleep_duration.minute
        if sleep_duration == 0:
            return 0
        time_spent_in_bed = self.average_time_spent_in_bed.hour * 60 + self.average_time_spent_in_bed.minute

        return round(sleep_duration / time_spent_in_bed * 100, 2)