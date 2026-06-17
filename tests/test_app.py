"""
Unit tests for Comp calendar scheduler
"""
import pytest
from datetime import time, timedelta
from io_comp.models import Event, TimeSlot
from io_comp.calendar_service import CalendarService

@pytest.fixture
def service():
    """Creates a service instance for each test with default hours (07:00-19:00)"""
    return CalendarService(day_start=time(7, 0), day_end=time(19, 0))

def test_full_day_available(service):
    """Verify that a completely empty day returns the full day window"""
    duration = timedelta(hours=1)
    results = service.find_available_slots([], ["Alice"], duration)
    # Ensure this is the only result returned
    assert results == ["07:00 - 18:00"]

def test_single_meeting_in_middle(service):
    """Verify that a meeting in the middle of the day creates exactly two precise windows"""
    # Meeting between 10:00 and 11:00
    events = [Event("Alice", "Meeting", TimeSlot(time(10, 0), time(11, 0)))]
    duration = timedelta(hours=1)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # Strict check of the entire list including order
    assert results == ["07:00 - 09:00", "11:00 - 18:00"]

def test_exact_fit_slot(service):
    """Verify that an exact fit (1h window for 1h meeting) returns a single time point"""
    events = [
        Event("Alice", "Morning", TimeSlot(time(7, 0), time(11, 0))),
        Event("Alice", "Afternoon", TimeSlot(time(12, 0), time(19, 0)))
    ]
    duration = timedelta(minutes=60)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # Ensure no "-" range is printed, only the start point
    assert results == ["11:00"]

def test_no_slots_available(service):
    """Verify that an empty list is returned when no sufficient time slot exists"""
    # Meeting covering almost the entire day
    events = [Event("Alice", "Busy", TimeSlot(time(7, 0), time(18, 30)))]
    duration = timedelta(hours=1)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # Ensure the list is completely empty
    assert results == []

def test_ignore_out_of_hours_events(service):
    """Verify that the algorithm ignores meetings outside working hours (07:00-19:00)"""
    events = [
        Event("Alice", "Early", TimeSlot(time(5, 0), time(6, 0))),
        Event("Alice", "Late", TimeSlot(time(19, 30), time(21, 0)))
    ]
    duration = timedelta(hours=1)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # Meetings should not affect the 07:00-19:00 window
    assert results == ["07:00 - 18:00"]

def test_multiple_attendees_overlap(service):
    """Verify that merging meetings from multiple attendees works correctly and returns an accurate list"""
    events = [
        Event("Alice", "M1", TimeSlot(time(9, 0), time(10, 0))),
        Event("Jack", "M2", TimeSlot(time(9, 30), time(10, 30)))
    ]
    duration = timedelta(minutes=30)
    results = service.find_available_slots(events, ["Alice", "Jack"], duration)
    
    # The merged busy period is 09:00-10:30
    # Slot 1: 07:00 to 08:30 (A 30m meeting must start by 08:30 to end by 09:00)
    # Slot 2: 10:30 to 18:30 (A 30m meeting must start by 18:30 to end by 19:00)
    expected = ["07:00 - 08:30", "10:30 - 18:30"]
    assert results == expected

def test_very_short_meeting_duration(service):
    """Verify that the algorithm correctly calculates windows for very short meetings"""
    events = [Event("Alice", "M1", TimeSlot(time(10, 0), time(10, 10)))]
    duration = timedelta(minutes=5)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # Slot 1: 07:00 to 09:55
    # Slot 2: 10:10 to 18:55
    assert results == ["07:00 - 09:55", "10:10 - 18:55"]