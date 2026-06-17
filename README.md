# Comp In-Office Coding Evaluation - Python

Welcome to the Python starter project for Comp's coding evaluation!

## Getting Started

### Prerequisites

You will need Python 3.8 or higher installed on your machine.

### Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Install the package in development mode:
```bash
pip install -e .
```

### Running the Application

To execute the app, you can run:
```bash
python -m io_comp.app
```

Or use the installed console script:
```bash
Comp-calendar
```

### Running Tests

To run the tests:
```bash
pytest
```

To run tests with verbose output:
```bash
pytest -v
```

## Project Structure

```
python-project/
├── io_Comp/              # Main application package
│   ├── __init__.py
│   └── app.py            # Application entry point
├── tests/                # Test directory
│   ├── __init__.py
│   └── test_app.py       # Unit tests
├── resources/            # Resources directory
│   └── calendar.csv      # Example calendar data
├── requirements.txt      # Python dependencies
├── setup.py             # Package configuration
└── README.md            # This file
```

## Your Task

Implement a calendar application that can find available time slots. See the main [README.md](../README.md) in the root directory for complete requirements.

### Method Signature

```python
from typing import List
from datetime import time, timedelta

def find_available_slots(person_list: List[str], event_duration: timedelta) -> List[time]:
    """
    Find all available time slots for a meeting with the given people and duration.

    Args:
        person_list: List of person names who should attend the meeting
        event_duration: Duration of the desired meeting

    Returns:
        List of start times when all persons are available
    """
    pass
```

## Tips

- The calendar data is available in `resources/calendar.csv`
- Python's `datetime` module provides useful classes like `time`, `datetime`, and `timedelta`
- Consider using classes to represent Calendar, Event, Person, etc.
- Follow PEP 8 style guidelines
- Write clean, modular, and well-documented code
- Don't forget to implement 2-3 meaningful tests!

Good luck!


## 🚀 My Implementation Notes

I designed this solution with **scalability**, **testability**, and **clean code** principles in mind.
Note on Return Type: I adjusted the return type to List[str] to properly format and support both time-ranges (e.g., '07:00 - 18:00') and exact-match timestamps as requested.

### 🏗️ Architecture
* **Decoupled Layers:** I separated the data-loading logic from the core algorithm. The `CSVEventProvider` handles file I/O, while the `CalendarService` focuses purely on scheduling logic.
* **Dependency Injection:** By injecting the data provider into the application flow, the system is now "infrastructure-agnostic"—switching from a CSV file to a Database or an API would require zero changes to the core logic.
* **Domain Modeling:** Used Python `dataclasses` for `Event` and `TimeSlot` to ensure type safety and code readability.

### 🧪 Quality Assurance & Testing
* **Strict Unit Testing:** Implemented a suite of automated tests using `pytest`.
* **Edge Case Coverage:**
    * **Merged Intervals:** Correctly handles overlapping meetings from multiple attendees.
    * **Boundary Constraints:** Ensures results stay strictly within the 07:00–19:00 window using `max/min` normalization.
    * **Precise Calculations:** Verifies that meeting durations are subtracted from the end of gaps to find the *latest possible* starting time.
    * **Format Integrity:** Validates that the output matches the required string format (e.g., handling single time points vs. ranges).

### ⚙️ Flexibility & Future Proofing
* **Configurable Parameters:** Working hours (`DAY_START`/`DAY_END`) are parameters of the service rather than hardcoded constants, allowing for future per-user customization.
* **Extensible Design:** The architecture is ready for future enhancements like timezone support, attendee priorities, or alternative output formatters (JSON/HTML).

---

### 🛠️ How to Run
- **App:** `python -m io_comp.app`
- **Tests:** `python -m pytest`