"""
This is the App entry point
"""
import os
import sys
from datetime import timedelta
from typing import List

# ייבוא הרכיבים מהחבילה הפנימית
from .calendar_service import CalendarService
from io_comp.data_loader import CSVEventProvider

def find_available_slots(person_list: List[str], event_duration: timedelta) -> List[str]:
    """
    המימוש המרכזי שנדרש בתרגיל.
    מחבר בין טעינת הנתונים מה-CSV לבין לוגיקת החישוב של הסרביס.
    """
    # חישוב נתיב דינמי לקובץ ה-CSV (נמצא רמה אחת מעל תיקיית io_comp)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_path, 'resources', 'calendar.csv')
    
    # 1. יצירת ספק הנתונים (Data Provider)
    provider = CSVEventProvider(csv_path)
    
    # 2. טעינת האירועים
    try:
        all_events = provider.get_events()
    except FileNotFoundError:
        print(f"Error: Could not find calendar file at {csv_path}")
        return []

    # 3. שימוש בסרביס לביצוע החישוב
    service = CalendarService()
    return service.find_available_slots(all_events, person_list, event_duration)


def main():
    """נקודת הכניסה להרצה של האפליקציה"""
      
    # 1. קבלת שמות המשתתפים (מופרדים בפסיק)
    people_input = input("Enter attendees names (comma separated, e.g. Alice, Jack): ")
    attendees = [name.strip() for name in people_input.split(",") if name.strip()]
    
    if not attendees:
        print("No attendees entered. Exiting.")
        return

    # 2. קבלת אורך הפגישה (עם ברירת מחדל)
    try:
        duration_input = input("Enter meeting duration in minutes [default 60]: ")
        duration_mins = int(duration_input) if duration_input.strip() else 60
        meeting_duration = timedelta(minutes=duration_mins)
    except ValueError:
        print("Invalid duration. Please enter a number.")
        return

    print(f"\nSearching for slots for {', '.join(attendees)} ({duration_mins} mins)...")
    
    results = find_available_slots(attendees, meeting_duration)
    
    if not results:
        print("No available slots found.")
    else:
        print("\nResults:")
        for slot in results:
            print(f"Starting Time of available slots: {slot}")


if __name__ == "__main__":
    main()

    



