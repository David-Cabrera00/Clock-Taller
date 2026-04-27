from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.clock_city import ClockCity


@dataclass
class _CityFrame:
    value: ClockCity
    next_city: Optional["_CityFrame"] = None
    previous_city: Optional["_CityFrame"] = None


class WorldClockCycle:
    def __init__(self) -> None:
        self._first_city: Optional[_CityFrame] = None
        self._current_city: Optional[_CityFrame] = None
        self._size = 0

    def add_city(self, city: ClockCity) -> None:
        frame = _CityFrame(city)

        if self._first_city is None:
            frame.next_city = frame
            frame.previous_city = frame
            self._first_city = frame
            self._current_city = frame
            self._size = 1
            return

        last_city = self._first_city.previous_city
        assert last_city is not None

        frame.next_city = self._first_city
        frame.previous_city = last_city
        last_city.next_city = frame
        self._first_city.previous_city = frame
        self._size += 1

    def current_city(self) -> Optional[ClockCity]:
        return self._current_city.value if self._current_city else None

    def next_city(self) -> Optional[ClockCity]:
        if self._current_city is None:
            return None

        self._current_city = self._current_city.next_city
        return self.current_city()

    def previous_city(self) -> Optional[ClockCity]:
        if self._current_city is None:
            return None

        self._current_city = self._current_city.previous_city
        return self.current_city()

    def select_city(self, city_name: str) -> Optional[ClockCity]:
        if self._first_city is None:
            return None

        cursor = self._first_city

        for _ in range(self._size):
            if cursor.value.name == city_name:
                self._current_city = cursor
                return cursor.value

            assert cursor.next_city is not None
            cursor = cursor.next_city

        return None

    def city_names(self) -> list[str]:
        names: list[str] = []

        if self._first_city is None:
            return names

        cursor = self._first_city

        for _ in range(self._size):
            names.append(cursor.value.name)
            assert cursor.next_city is not None
            cursor = cursor.next_city

        return names

    def __len__(self) -> int:
        return self._size