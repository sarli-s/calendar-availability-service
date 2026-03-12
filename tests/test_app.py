"""
Unit tests for Comp calendar scheduler
"""
import pytest
from datetime import time, timedelta
from io_comp.models import Event, TimeSlot
from io_comp.calendar_service import CalendarService

@pytest.fixture
def service():
    """יוצר מופע של הסרביס לכל טסט עם שעות ברירת המחדל (07:00-19:00)"""
    return CalendarService()

def test_full_day_available(service):
    """בדיקה שביום ריק לגמרי חוזר בדיוק חלון אחד של כל היום"""
    duration = timedelta(hours=1)
    results = service.find_available_slots([], ["Alice"], duration)
    # מוודא שזו התוצאה היחידה שחוזרת
    assert results == ["07:00 - 18:00"]

def test_single_meeting_in_middle(service):
    """בדיקה שפגישה באמצע היום מייצרת בדיוק שני חלונות פנויים מדויקים"""
    # פגישה בין 10:00 ל-11:00
    events = [Event("Alice", "Meeting", TimeSlot(time(10, 0), time(11, 0)))]
    duration = timedelta(hours=1)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # בדיקה קשיחה של כל הרשימה כולל הסדר
    assert results == ["07:00 - 09:00", "11:00 - 18:00"]

def test_exact_fit_slot(service):
    """בדיקה שמקרה של התאמה מדויקת (חלון של שעה לפגישה של שעה) מחזיר שעה בודדת"""
    events = [
        Event("Alice", "Morning", TimeSlot(time(7, 0), time(11, 0))),
        Event("Alice", "Afternoon", TimeSlot(time(12, 0), time(19, 0)))
    ]
    duration = timedelta(minutes=60)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # מוודא שלא מודפס טווח עם "-" אלא רק נקודת ההתחלה
    assert results == ["11:00"]

def test_no_slots_available(service):
    """בדיקה שחוזרת רשימה ריקה כשאין שום חלון זמן מספיק גדול"""
    # פגישה כמעט על כל היום
    events = [Event("Alice", "Busy", TimeSlot(time(7, 0), time(18, 30)))]
    duration = timedelta(hours=1)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # מוודא שהרשימה ריקה לחלוטין
    assert results == []

def test_ignore_out_of_hours_events(service):
    """בדיקה שהאלגוריתם מתעלם מפגישות מחוץ לשעות העבודה (07:00-19:00)"""
    events = [
        Event("Alice", "Early", TimeSlot(time(5, 0), time(6, 0))),
        Event("Alice", "Late", TimeSlot(time(19, 30), time(21, 0)))
    ]
    duration = timedelta(hours=1)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # הפגישות לא אמורות להשפיע על חלון ה-07:00-19:00
    assert results == ["07:00 - 18:00"]

def test_multiple_attendees_overlap(service):
    """בדיקה שמיזוג פגישות של מספר אנשים שונים עובד נכון ומחזיר רשימה מדויקת"""
    events = [
        Event("Alice", "M1", TimeSlot(time(9, 0), time(10, 0))),
        Event("Jack", "M2", TimeSlot(time(9, 30), time(10, 30)))
    ]
    duration = timedelta(minutes=30)
    results = service.find_available_slots(events, ["Alice", "Jack"], duration)
    
    # החלק התפוס הממוזג הוא 09:00-10:30
    # חלון 1: 07:00 עד 08:30 (כי פגישה של 30 דק צריכה להתחיל לכל המאוחר ב-08:30 כדי לסיים ב-09:00)
    # חלון 2: 10:30 עד 18:30 (כי פגישה של 30 דק צריכה להתחיל לכל המאוחר ב-18:30 כדי לסיים ב-19:00)
    expected = ["07:00 - 08:30", "10:30 - 18:30"]
    assert results == expected

def test_very_short_meeting_duration(service):
    """בדיקה שהאלגוריתם מחשב נכון חלונות לפגישה קצרה מאוד"""
    events = [Event("Alice", "M1", TimeSlot(time(10, 0), time(10, 10)))]
    duration = timedelta(minutes=5)
    results = service.find_available_slots(events, ["Alice"], duration)
    
    # חלון 1: 07:00 עד 09:55
    # חלון 2: 10:10 עד 18:55
    assert results == ["07:00 - 09:55", "10:10 - 18:55"]