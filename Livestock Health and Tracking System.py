print("==========Livestock Health & Tracking System==========")

from datetime import date


# ---------------------------------------------------------------- Class 1
class Animal:
    """One animal and its health history (Task 1: attributes + methods)."""

    EVENT_TYPES = ("Checkup", "Vaccination", "Treatment", "Illness", "Recovered")
    CHECKUP_INTERVAL_DAYS = 180   # an animal with no event for this long is flagged
    _counter = 0                  # class attribute used to generate unique IDs

    def __init__(self, tag, species, age_months):
        tag = tag.strip()
        species = species.strip().title()
        if not tag:
            raise ValueError("Tag label cannot be empty.")
        if not species.replace(" ", "").replace("-", "").isalpha():
            raise ValueError("Species must be a name using letters only (e.g. Cattle, Goat).")
        if age_months <= 0:
            raise ValueError("Age in months must be above 0.")
        Animal._counter += 1
        self.animal_id = f"A{Animal._counter:03d}"
        self.tag = tag                       # e.g. "Cow 7" (no farmer name)
        self.species = species
        self.age_months = age_months
        self.registered = date.today().isoformat()
        self.health_log = ()                 # tuple of (date, event_type, note) tuples

    # ---- instance methods (Task 3)
    def record_event(self, event_type, note=""):
        """Record a health event as an immutable tuple: (date, event_type, note).
        Tuples cannot be changed, so a new tuple of events is built."""
        event_type = self.normalize_event(event_type)
        new_event = (date.today().isoformat(), event_type, note.strip())
        self.health_log = self.health_log + (new_event,)

    def update_record(self, tag=None, age_months=None):
        if tag:
            self.tag = tag.strip()
        if age_months is not None:
            if age_months <= 0:
                raise ValueError("Age in months must be above 0.")
            self.age_months = age_months

    def current_status(self):
        """Status comes from the most recent health event."""
        if not self.health_log:
            return "No records"
        return self.status_from_event(self.health_log[-1][1])

    def days_since_last_event(self):
        last_date = self.health_log[-1][0] if self.health_log else self.registered
        return (date.today() - date.fromisoformat(last_date)).days

    def attention_reason(self):
        """Return why this animal needs attention, or '' if it does not."""
        if self.current_status() in ("Sick", "Under treatment"):
            return f"Status: {self.current_status()}"
        if self.days_since_last_event() > Animal.CHECKUP_INTERVAL_DAYS:
            return f"No health event for {self.days_since_last_event()} days"
        return ""

    def display_info(self):
        print(f"ID: {self.animal_id} | {self.tag} | {self.species} | "
              f"{self.age_months} months ({self.age_group(self.age_months)}) | "
              f"Status: {self.current_status()}")
        for event_date, event_type, note in self.health_log:
            line = f"    - {event_date}: {event_type}"
            print(line + (f" ({note})" if note else ""))

    # ---- class methods (Task 3)
    @classmethod
    def from_string(cls, text):
        """Create an Animal from 'tag,species,age_months' e.g. 'Cow 7, Cattle, 24'."""
        parts = text.split(",")
        if len(parts) != 3:
            raise ValueError("Use the format: tag,species,age_months")
        try:
            age = int(parts[2])
        except ValueError:
            raise ValueError("Age in months must be a whole number.")
        return cls(parts[0], parts[1], age)

    # ---- static methods (Task 3)
    @staticmethod
    def age_group(age_months):
        """General age group only; real stages differ for each species."""
        if age_months < 12:
            return "Young"
        if age_months < 96:
            return "Adult"
        return "Senior"

    @staticmethod
    def status_from_event(event_type):
        """Turn the latest event type into a simple health status."""
        if event_type == "Illness":
            return "Sick"
        if event_type == "Treatment":
            return "Under treatment"
        return "Healthy"

    @staticmethod
    def normalize_event(event_type):
        """Check an event name (any capitalisation) and return the standard form."""
        clean = event_type.strip().title()
        if clean not in Animal.EVENT_TYPES:
            raise ValueError("Event must be one of: " + ", ".join(Animal.EVENT_TYPES) + ".")
        return clean


# ---------------------------------------------------------------- Class 2
class LivestockRegistry:
    """Stores many Animal objects in a dictionary keyed by animal ID
    (Task 2: one data structure + add/display functions)."""

    def __init__(self, farm_name):
        self.farm_name = farm_name
        self.animals = {}  # {animal_id: Animal}

    def add_animal(self, animal):
        self.animals[animal.animal_id] = animal
        print(f"Added {animal.tag} ({animal.species}) with ID {animal.animal_id}.")

    def find(self, animal_id):
        return self.animals.get(animal_id.strip().upper())

    def display_all(self):
        print(f"\n=== {self.farm_name}: {len(self.animals)} animal(s) ===")
        if not self.animals:
            print("No records yet.")
        for animal in self.animals.values():
            animal.display_info()

    def remove_animal(self, animal_id):
        """Delete a record (e.g. animal sold or died; also supports privacy)."""
        removed = self.animals.pop(animal_id.strip().upper(), None)
        if removed is None:
            print("Animal not found.")
            return False
        print(f"Record {removed.animal_id} ({removed.tag}) removed.")
        return True

    def display_alerts(self):
        """Show animals that are sick, under treatment or overdue for a checkup."""
        print(f"\n=== Health alerts: {self.farm_name} ===")
        found = 0
        for animal in self.animals.values():
            reason = animal.attention_reason()
            if reason:
                found += 1
                print(f"{animal.animal_id} | {animal.tag} | {animal.species} | {reason}")
        if found == 0:
            print("No animals need attention.")
        return found

    def species_summary(self):
        """Count the animals of each species, whatever species were entered.
        The species found so far are kept in a tuple, so no new list or
        dictionary is needed."""
        print(f"\n=== Species summary: {self.farm_name} ===")
        if not self.animals:
            print("No records yet.")
        found = ()
        for animal in self.animals.values():
            if animal.species not in found:
                found = found + (animal.species,)
        for species in found:
            total = sum(1 for a in self.animals.values() if a.species == species)
            print(f"{species}: {total}")


# ---------------------------------------------------------------- Demo / menu
def demo(registry):
    """Optional sample data. Not run by default; call demo(registry) to load it."""
    a1 = Animal("Cow 7", "Cattle", 36)
    a2 = Animal.from_string("Goat 2, Goat, 10")   # class method
    registry.add_animal(a1)
    registry.add_animal(a2)
    a1.record_event("Vaccination", "FMD vaccine")  # instance method
    a2.record_event("Illness", "Not eating")
    a1.update_record(age_months=37)
    registry.display_all()


def menu(registry):
    while True:
        print("\n1. Add animal  2. Record health event  3. Show all")
        print("4. Health alerts  5. Species summary  6. Remove animal  7. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            try:
                text = input("Tag,species,age in months (e.g. Cow 7,Cattle,24): ")
                registry.add_animal(Animal.from_string(text))
            except ValueError as error:
                print(f"Error: {error}")
        elif choice == "2":
            animal = registry.find(input("Animal ID: "))
            if animal:
                try:
                    print("Events: " + ", ".join(Animal.EVENT_TYPES))
                    event = input("Event: ")
                    note = input("Short note (optional, no personal details): ")
                    animal.record_event(event, note)
                    print(f"Recorded. {animal.tag} is now: {animal.current_status()}.")
                except ValueError as error:
                    print(f"Error: {error}")
            else:
                print("Animal not found.")
        elif choice == "3":
            registry.display_all()
        elif choice == "4":
            registry.display_alerts()
        elif choice == "5":
            registry.species_summary()
        elif choice == "6":
            registry.remove_animal(input("Animal ID to remove: "))
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    registry = LivestockRegistry("Community Farm")
    menu(registry)  # starts empty; use demo(registry) for sample data
