import abc

from datetime import timedelta
from typing_extensions import Self

from pydantic import computed_field

from src.domain import note


class NoteDurations(note.BaseNoteDurations, abc.ABC):
    @computed_field(title="Длительность сна")  # type: ignore[misc]
    @property
    def _sleep_duration(self: Self) -> timedelta:
        sleep_duration = timedelta(
            hours=self.woke_up.hour - self.fell_asleep.hour,
            minutes=self.woke_up.minute - self.fell_asleep.minute,
        )
        return timedelta(seconds=sleep_duration.seconds)

    @computed_field(  # type: ignore[misc]
        title="Длительность сна за вычетом времени без сна",
    )
    @property
    def _sleep_duration_minus_no_sleep(self: Self) -> timedelta:
        if self._no_sleep_duration >= self._sleep_duration:
            return timedelta(0)
        sleep_duration_minus_no_sleep = (
            self._sleep_duration - self._no_sleep_duration
        )
        return timedelta(seconds=sleep_duration_minus_no_sleep.seconds)

    @computed_field(  # type: ignore[misc]
        title="Длительность времени, проведенного в постели.",
    )
    @property
    def _in_bed_duration(self: Self) -> timedelta:
        sleep_duration = timedelta(
            hours=self.got_up.hour - self.went_to_bed.hour,
            minutes=self.got_up.minute - self.went_to_bed.minute,
        )
        return timedelta(seconds=sleep_duration.seconds)

    @computed_field(title="Длительность отсутствия сна")  # type: ignore[misc]
    @property
    def _no_sleep_duration(self: Self) -> timedelta:
        return timedelta(
            hours=self.no_sleep.hour,
            minutes=self.no_sleep.minute,
        )
