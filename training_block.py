from workout import Workout
from workout_templates import WorkoutTemplate


class TrainingBlock():


    # each training "block" will have a starting date attributed to it
    def __init__(self, starting_date, workouts_per_week):
        # the starting date needs to be in "Month-day-year" format
        self.starting_date = starting_date
        self.workouts_per_week = workouts_per_week
        self.workouts = []
        self.templates = [] # This will be a list of workout templates. ie, "Leg Day", "Upper Body", etc.


    # each workout will have a date it was done and a dictionary that will come from the gui code. 
    # This dictionary will have all the exersices, sets, reps, and weight for the workout.
    def add_workout(self, workout):
        """Allows you to add a new workout to the choosen TrainingBlock"""

        self.workouts.append(workout)
        # workout.print_workout()


    def add_template(self, name, exercises):
        self.templates.append(WorkoutTemplate(name, exercises))


    def to_dict(self):
        """Converts the current TrainingBlock to a dict for saving."""

        return {
            "starting_date" : self.starting_date,
            "workouts_per_week" : self.workouts_per_week,
            "workouts" : [workout.to_dict() for workout in self.workouts],
            "templates" : [template.to_dict() for template in self.templates]
        }
    

    @classmethod
    def from_dict(cls, data):
        """Converts a dictionary with data into a TrainingBlock"""

        block = cls(data["starting_date"], data["workouts_per_week"])
        # block.workouts = [Workout(**workout) for workout in data["workouts"]]
        block.workouts = [Workout.from_dict(workout) for workout in data["workouts"]]
        block.templates = [WorkoutTemplate(**template) for template in data["templates"]]

        return block
    

    def print_block(self):
        """Prints the current TrainingBlock in a readable format."""
        print(f"Training Block starting on: {self.starting_date}")
        print(f"Workouts per week: {self.workouts_per_week}")
        print("Current workout templates:")
        for template in self.templates:
            template.print_template()

            