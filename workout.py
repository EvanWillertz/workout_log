from datetime import date

class Workout:
    def __init__(self, template_name):
        self.template_name = template_name
        self.date = str(date.today().strftime("%B %#d, %Y"))
        self.entries = {}  # {exercise_name: [[reps, weight], ...]}

    def add_entry(self, entries):
        self.entries = entries


    def print_workout(self):
        print(f"Workout Date: {self.date}")
        print(f"Workout Template: {self.template_name}")
        for exercise, entries in self.entries.items():
            print(f"Exercise: {exercise}")
            for num, entry in enumerate(entries):
                reps, weight = entry
                print(f"Set:{num+1} -> Reps: {reps}, Weight: {weight}")

    def to_dict(self):
        """Converts the current Workout to a dict for saving."""
        return {
            "date": self.date,
            "template_name": self.template_name,
            "entries": self.entries
        }
    

    @classmethod
    def from_dict(cls, data):
        obj = cls(data["template_name"])
        obj.date = data["date"]
        obj.entries = data["entries"]
        return obj
