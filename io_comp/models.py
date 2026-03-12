from dataclasses import dataclass
from datetime import time, datetime, timedelta

@dataclass(frozen=True)
class TimeSlot:
    start: time
    end: time

    def __repr__(self):
        return f"{self.start.strftime('%H:%M')} - {self.end.strftime('%H:%M')}"

@dataclass(frozen=True)
class Event:
    person_name: str
    subject: str
    slot: TimeSlot