import datetime as dt
import operator as op
import statistics as st

from typing import Generator
from typing_extensions import Self

from pydantic import computed_field

from src.domain import note as nt, week as wk


class WeeklyAverageDurations(wk.BaseWeeklyAverageDurations):
    def __compute_average_duration(
        self: Self,
        duration_name: str,
    ) -> Generator[dt.timedelta, None, None]:
        all_durations_in_seconds_of_week: Generator[int, None, None] = (
            op.attrgetter(f"{duration_name}.seconds")(note)
            for note in self
            if isinstance(note, nt.BaseNoteDurations)
        )
        yield dt.timedelta(seconds=st.mean(all_durations_in_seconds_of_week))

    @computed_field(title="Продолжительность недели")  # type: ignore[misc]
    @property
    def _duration_of_week(self: Self) -> wk.int_duration_of_week:
        return len(self)

    @computed_field(title="Средняя длительность сна за неделю")  # type: ignore[misc]
    @property
    def _average_weekly_sleep_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration("_sleep_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность времени, проведенного в постели, за неделю.",
    )
    @property
    def _average_weekly_in_bed_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration("_in_bed_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность отсутствия сна за неделю",
    )
    @property
    def _average_weekly_no_sleep_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration("_no_sleep_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность сна за неделю за вычетом времени без сна",
    )
    @property
    def _average_weekly_sleep_duration_minus_no_sleep(
        self: Self,
    ) -> dt.timedelta:
        return next(
            self.__compute_average_duration("_sleep_duration_minus_no_sleep"),
        )