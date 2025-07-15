class WorkoutTemplate:
    def __init__(self, name, exercises):
        self.name = name
        self.exercises = exercises

    def to_dict(self):
        """Converts the current WorkoutTemplate to a dict for saving."""
        return {
            "name": self.name,
            "exercises": self.exercises
        }

    def print_template(self):
        """Prints the workout template in a readable format."""
        print(f"Workout Template: {self.name}")
        print("Exercises:")
        for exercise in self.exercises:
            print(f" - {exercise}")

