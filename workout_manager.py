import json
import os
from training_block import TrainingBlock
import bisect
import shutil
import sys
import platform



def resource_path(relative_path):
    try:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))  # PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_user_data_path(filename: str) -> str:

    """Cross-platform user-specific app data folder"""
    system = platform.system()
    if system == "Windows":
        base_dir = os.getenv("APPDATA") or os.path.expanduser("~\\AppData\\Roaming")
    elif system == "Darwin":  # macOS
        base_dir = os.path.expanduser("~/Library/Application Support")
    else:  # Linux and others
        base_dir = os.path.expanduser("~/.local/share")


    app_data_dir = os.path.join(base_dir, "EvanWorkoutApp")
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, filename)


def setup_default_json(file_name: str):
    """Copies a default JSON file to the user's app data folder if it's not already there."""
    destination = get_user_data_path(file_name)
    if not os.path.exists(destination):
        default_file = resource_path(f"default_{file_name}")
        shutil.copy(default_file, destination)
    return destination
    

class WorkoutManager():
    # DATA_FILE = "training_block_data.json"
    # TOTAL_DATA_FILE = "training_data.json"
    # this is for the PyInstaller executable
    # so that the data files are in the same directory as the executable
    DATA_FILE = setup_default_json("training_block_data.json")
    TOTAL_DATA_FILE = setup_default_json("training_data.json")


    def __init__(self):
        """Manages multiple TrainingBlocks and handles data persistence."""
        # print("Initializing WorkoutManager...")

        self.all_exercises = []

        self.over_time_tracker = {}
        self.training_blocks = []
        self.load_data()
        

    def add_training_block(self, starting_date, workouts_per_week):
        """Adds a new TrainingBlock to the system."""

        new_block = TrainingBlock(starting_date, workouts_per_week)
        self.training_blocks.append(new_block)

        self.save_data()

    def add_template_to_block(self, block, name, exercises):
        """Adds a new workout template to a specific TrainingBlock."""

        block.add_template(name, exercises)
        self.save_data()


    def add_exercise(self, exercise_name):
        """Adds a new exercise to the all_exercises list."""

        if exercise_name not in self.all_exercises:
            bisect.insort(self.all_exercises, exercise_name) # this adds it in alphabetical order!

            # adds the exercise to the tracking system
            self.over_time_tracker[exercise_name] = {"Volume" : [[], []]}
            # adds a new entry in the personal bests dictionary for the new exercise
            self.over_time_tracker["Personal Bests"][exercise_name] = [0, 0, ""]
            self.save_tracker_data()


            # print(f"Exercise '{exercise_name}' added.")
        else:
            print(f"Exercise '{exercise_name}' already exists.")


    def save_data(self):
        """Saves all training blocks to JSON."""
        
        # print("Saving data...")
        data_to_save = {
        "all_exercises": self.all_exercises,  # e.g., a list stored in your class
        "training_blocks": [block.to_dict() for block in self.training_blocks]
        }
        with open(self.DATA_FILE, "w") as f:
            json.dump(data_to_save, f, indent=4)

    def save_tracker_data(self):
        with open(self.TOTAL_DATA_FILE, "w") as f:
            json.dump(self.over_time_tracker, f, indent=4)

    
    def add_workout_to_tracker(self, workout):
        workout_date = workout.date

        total_reps = 0
        total_volume = 0

        # iterating over all the exercises in the workout
        for name, entry in workout.entries.items():
            # list of the best sets of each particular rep range reached
            reps = [] 
            weights = []

            all_reps = 0
            all_weight = 0

            # iterating over each of the sets in the entry
            for rep, weight in entry:

                # add up the number of reps and total weight moved
                all_reps += int(rep)
                all_weight += int(weight) * int(rep)

                # if we've already seen this rep number, then compare the weights
                if rep in reps:
                    idx = reps.index(rep)
                    # if the new weigth is more than the already found weight, replace
                    if weights[idx] < weight:
                        weights[idx] = weight
                # if we have not seen this rep number yet, add to lists
                else:
                    reps.append(rep)
                    weights.append(weight)


            # now to add this new weight info for each found rep count to the tracker
            cur_exercise = self.over_time_tracker[name] # dict of current exercise {rep # : [[weight], [corrisponding date]], ...}
            cur_exercise['Volume'][0].append(all_weight) # add the volume for this exercise
            cur_exercise['Volume'][1].append(str(workout_date)) # add the date

            # iterating over each rep range
            for i, rep in enumerate(reps):
                # see if rep number has been added to dict yet
                rep = str(rep) # convert to string for dictionary key

                if rep in cur_exercise.keys():
                    rep_running_list = cur_exercise[rep]

                    rep_running_list[0].append(weights[i]) # add the weight for that rep number
                    rep_running_list[1].append(str(workout_date)) # add the date when that was repped
                # if not seen rep number yet
                else:
                    cur_exercise[rep] = [[weights[i]], [str(workout_date)]]


            # sets the new heaviest weight lifted and for the number of reps to the dictionary
            heaviest_set = int(max(weights))
            if heaviest_set > self.over_time_tracker["Personal Bests"][name][1]: # because the lists is [rep #, weight]
                self.over_time_tracker["Personal Bests"][name][1] = heaviest_set
                self.over_time_tracker["Personal Bests"][name][0] = reps[weights.index(max(weights))]
                self.over_time_tracker["Personal Bests"][name][2] = str(workout_date) # also add the date of the personal best
            # this is if the heaviest set matches the current personal best, but the reps are more than the previous best
            elif heaviest_set == self.over_time_tracker["Personal Bests"][name][1] and reps[weights.index(max(weights))] >= self.over_time_tracker["Personal Bests"][name][0]:
                self.over_time_tracker["Personal Bests"][name][1] = heaviest_set
                self.over_time_tracker["Personal Bests"][name][0] = reps[weights.index(max(weights))]
                self.over_time_tracker["Personal Bests"][name][2] = str(workout_date) # also add the date of the personal best


            # adding the total rep number and weight
            self.over_time_tracker["Stats"]["Total Rep #"] += all_reps
            self.over_time_tracker["Stats"]["Total Volume"] += all_weight
            total_reps += all_reps
            total_volume += all_weight

        # adding the number of reps and volume for the workout to the over time tracker
        self.over_time_tracker["Stats"]["Rep # Per Workout"][0].append(total_reps)
        self.over_time_tracker["Stats"]["Rep # Per Workout"][1].append(workout_date)
        self.over_time_tracker["Stats"]["Volume Per Workout"][0].append(total_volume)
        self.over_time_tracker["Stats"]["Volume Per Workout"][1].append(workout_date)

        self.save_tracker_data()


    def load_data(self):
        """Loads training blocks from JSON if available."""
        print("Loading data...")
        # Check if the file exists and is not empty
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as f:
                try:
                    print("Loading data from file...")
                    data = json.load(f)   # load the data from the file                    
                    self.all_exercises = data.get("all_exercises", [])
                    self.training_blocks = [TrainingBlock.from_dict(block) for block in data.get("training_blocks", [])]
                except json.JSONDecodeError:
                    return []    

        # loading in the data for the over time tracker
        if os.path.exists(self.TOTAL_DATA_FILE):
            with open(self.TOTAL_DATA_FILE, "r") as f:
                try:
                    print("Loading data for tracker...")
                    data = json.load(f)   # load the data from the file
                    self.over_time_tracker = data
                    # print(self.over_time_tracker.keys())
                except json.JSONDecodeError:
                    return []
    

    def print_training_blocks(self):
        for idx, block in enumerate(self.training_blocks):
            print(f"\nTraining Block {idx + 1}:")
            print(f"Training Block starting on {block.starting_date} with {block.workouts_per_week} workouts per week.")
            print("Templates:")
            for template in block.templates:
                template.print_template()


    def print_workouts_from_block(self):
        """Prints all workouts from a specific training block."""
        block_idx = int(input("Choose a training block to view workouts from (1, 2, etc.): ")) - 1
        block = self.training_blocks[block_idx]
        print(f"\nWorkouts for Training Block starting on {block.starting_date}:")
        for workout in block.workouts:
            workout.print_workout()
    

    def print_all_exercises(self):
        """Prints all exercises across all training blocks."""
        print("All Exercises:")
        for exercise in self.all_exercises:
            print(f"- {exercise}")

    