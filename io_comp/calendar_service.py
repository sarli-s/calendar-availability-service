from typing import List
from datetime import time, datetime, timedelta
from .models import TimeSlot, Event

class CalendarService:
    def __init__(self, day_start=time(7, 0), day_end=time(19, 0)):
        self.day_start = day_start
        self.day_end = day_end
        
    def find_available_slots(self, events: List[Event], person_list: List[str], duration: timedelta) -> List[str]:
        # 1. סינון אירועים רלוונטיים
        relevant_slots = [e.slot for e in events if e.person_name in person_list]
        
        # 2. מיזוג אירועים חופפים
        merged_busy = self._merge_intervals(relevant_slots)

        # 3. מציאת חלונות פנויים
        available_ranges = []
        duration_mins = duration.total_seconds() / 60
        current_time = self.day_start

        for busy_slot in merged_busy:
            # התעלמות מאירועים שמסתיימים לפני תחילת היום או מתחילים אחרי סוף היום
            if busy_slot.end <= self.day_start:
                continue
            if busy_slot.start >= self.day_end:
                break

            # חישוב הפער בין הזמן הנוכחי לתחילת הפגישה הבאה
            gap_start = max(current_time, self.day_start)
            gap_end = min(busy_slot.start, self.day_end)
            
            gap_duration = self._diff_minutes(gap_start, gap_end)
            
            if gap_duration >= duration_mins:
                # חישוב נקודת ההתחלה האחרונה האפשרית
                latest_start = self._add_minutes(gap_end, -int(duration_mins))
                
                if gap_start == latest_start:
                    available_ranges.append(f"{gap_start.strftime('%H:%M')}")
                else:
                    available_ranges.append(f"{gap_start.strftime('%H:%M')} - {latest_start.strftime('%H:%M')}")
            
            # עדכון הזמן הנוכחי לסוף הפגישה (כדי לא לחזור אחורה)
            if busy_slot.end > current_time:
                current_time = busy_slot.end

        # בדיקה אחרונה מסיבת הסיום ועד סוף היום (19:00)
        final_check_start = max(current_time, self.day_start)
        if final_check_start < self.day_end:
            final_gap = self._diff_minutes(final_check_start, self.day_end)
            if final_gap >= duration_mins:
                latest_start = self._add_minutes(self.day_end, -int(duration_mins))
                if final_check_start == latest_start:
                    available_ranges.append(f"{final_check_start.strftime('%H:%M')}")
                else:
                    available_ranges.append(f"{final_check_start.strftime('%H:%M')} - {latest_start.strftime('%H:%M')}")

        return available_ranges

    def _merge_intervals(self, slots: List[TimeSlot]) -> List[TimeSlot]:
        if not slots: return []
        sorted_slots = sorted(slots, key=lambda x: x.start)
        merged = []
        current = sorted_slots[0]
        
        for next_slot in sorted_slots[1:]:
            if next_slot.start <= current.end:
                if next_slot.end > current.end:
                    current = TimeSlot(current.start, next_slot.end)
            else:
                merged.append(current)
                current = next_slot
        merged.append(current)
        return merged

    def _diff_minutes(self, t1: time, t2: time) -> int:
        return (t2.hour * 60 + t2.minute) - (t1.hour * 60 + t1.minute)

    def _add_minutes(self, t: time, minutes: int) -> time:
        full_dt = datetime.combine(datetime.today(), t) + timedelta(minutes=minutes)
        return full_dt.time()