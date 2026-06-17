import csv
from typing import List
from .models import Event, TimeSlot
from datetime import datetime


class EventProvider:
    """Base interface for loading events"""
    def get_events(self) -> List[Event]:
        raise NotImplementedError


class CSVEventProvider(EventProvider):
    """CSV-specific implementation for event loading"""
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_events(self) -> List[Event]:
        events = []
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row: continue
                name, subject, start_str, end_str = [item.strip() for item in row]
                start = datetime.strptime(start_str, "%H:%M").time()
                end = datetime.strptime(end_str, "%H:%M").time()
                events.append(Event(name, subject, TimeSlot(start, end)))
        return events