# Livestock Health & Tracking System

A simple Python program that helps small farms and farming cooperatives register their animals, record health events (checkups, vaccinations, illness, treatment) and see which animals need attention. Built with Object-Oriented Programming (OOP) Concepts.
**Domain:** Agriculture  
**Problem:** On many small farms, animal health is tracked from memory or in notebooks. Sick animals can be missed, and vaccinations or checkups can be forgotten. This tool gives farms a free, lightweight way to keep health records and get alerts, on any computer with Python.

## Features

- Register an animal (tag label, species, age in months) with an automatically generated ID
- Record health events: Checkup, Vaccination, Treatment, Illness, Recovered
- Work out each animal's current status (Healthy, Sick, Under treatment) from its latest event
- Show a health alert list of animals that are sick, under treatment, or have had no health event for 180 days
- Accept any species (cattle, goat, sheep, rabbit, and so on) and show a summary count for each species entered
- Remove an animal's record (for example when an animal is sold)
- Checks every input and shows clear error messages instead of crashing

## How to Run

1. Install Python 3.8 or later.
2. Download or clone this repository:
 
3. Run the program:
   ```
   python livestock_tracker.py
   ```

The program starts empty and opens a menu. You add your own animals:

```
1. Add animal  2. Record health event  3. Show all
4. Health alerts  5. Species summary  6. Remove animal  7. Exit
```

Sample data is available but does not run by default: call `demo(registry)` in the last lines of the file to load it.

## Project Structure

| File | Purpose |
|------|---------|
| `livestock_tracker.py` | Classes, demo and menu |
| `README.md` | Documentation |
| `LICENSE` | MIT open-source licence |

## OOP Concepts Used

### Task 1: Classes and Objects
- **`Animal`**: attributes `animal_id`, `tag`, `species`, `age_months`, `registered`, `health_log`; methods `record_event()`, `update_record()`, `current_status()`, `days_since_last_event()`, `attention_reason()`, `display_info()`
- **`LivestockRegistry`**: attributes `farm_name`, `animals`; methods `add_animal()`, `find()`, `display_all()`, `remove_animal()`, `display_alerts()`, `species_summary()`
- The registry holds and manages `Animal` objects, which demonstrates interaction between objects. For example, `display_alerts()` asks each animal for its `attention_reason()`, and `species_summary()` reads each animal's species.

### Task 2: Data Structure
- A **dictionary** (`{animal_id: Animal}`) stores all animals, so any record can be found instantly by its ID.
- `add_animal()` and `display_all()` add and display records.
- **Bonus (tuples):** each health event is a **tuple** `(date, event_type, note)`, and an animal's `health_log` is a tuple of these. Tuples cannot be changed, so each new event builds a new tuple and a saved record cannot be altered by accident. The list of allowed event types is also a tuple, and the species summary collects the species it finds in a tuple. The dictionary is the only data structure holding the animal objects.

### Task 3: Methods
| Type | Method | Purpose |
|------|--------|---------|
| Instance | `record_event()`, `update_record()`, `current_status()`, `days_since_last_event()`, `attention_reason()`, `display_info()` | Work on one animal's data |
| Class (`@classmethod`) | `Animal.from_string("Cow 7, Cattle, 24")` | Alternative way to create an animal from text |
| Static (`@staticmethod`) | `Animal.age_group()` | Converts an age in months to Young, Adult or Senior |
| Static (`@staticmethod`) | `Animal.status_from_event()` | Turns an event type into a simple health status |
| Static (`@staticmethod`) | `Animal.normalize_event()` | Checks an event name typed in any capitalisation |

## Digital Public Goods (DPG) Alignment

| DPG Principle | How this project meets it |
|---------------|---------------------------|
| **Open-source** | The full source code is public on GitHub under the MIT licence, so anyone can use, study, modify and share it. |
| **Inclusive and accessible design** | Plain-language prompts, a numbered menu, and clear error messages that say how to fix a mistake. Any species can be entered, in any capitalisation (for example `goat` or `Goat` are treated as the same). It runs on any low-spec computer, needs no internet connection and has no cost. |
| **Privacy-respecting** | No personal data about farmers is stored. Each record is an animal tag label (such as "Cow 7"), a species, an age and health events. There are no names, phone numbers, addresses, ID numbers or GPS locations, and the note prompt reminds users not to enter personal details. Data is kept in memory only and is not sent anywhere. A record can be removed at any time. |
| **Modular and reusable** | `Animal` and `LivestockRegistry` are separate, self-contained classes. They can be imported into other projects, for example a crop tracker or a veterinary visit planner, without changing the code. The start block means importing the file does not run the menu. |

## Sample Output

```
1. Add animal  2. Record health event  3. Show all
4. Health alerts  5. Species summary  6. Remove animal  7. Exit
Choose: 1
Tag,species,age in months (e.g. Cow 7,Cattle,24): Goat 2,goat,10
Added Goat 2 (Goat) with ID A001.

Choose: 2
Animal ID: a001
Events: Checkup, Vaccination, Treatment, Illness, Recovered
Event: illness
Short note (optional, no personal details): Not eating
Recorded. Goat 2 is now: Sick.

Choose: 3

=== Community Farm: 1 animal(s) ===
ID: A001 | Goat 2 | Goat | 10 months (Young) | Status: Sick
    - 2026-10-18: Illness (Not eating)

Choose: 4

=== Health alerts: Community Farm ===
A001 | Goat 2 | Goat | Status: Sick
```

## Limitations and Future Improvements

- Records are lost when the program closes (kept in memory for privacy). A future version could add optional local storage.
- Age groups and the 180-day checkup interval are general values. Real schedules differ for each species, so a future version could use species-specific values.
- Add a graphical interface and local-language support (e.g. Krio).

## Author

Mohamed Paye


## Licence

Released under the [MIT Licence](LICENSE).
