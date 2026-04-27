from dataclasses import dataclass


@dataclass
class ClockCity:
    name: str
    utc_offset_hours: int