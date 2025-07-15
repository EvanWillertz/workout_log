from workoutapp_gui import *
from workout_manager import WorkoutManager


def run_workout_app():
    """Run the workout application."""
    
    manager = WorkoutManager()
    app = WorkoutAppGUI(manager)
    app.mainloop()



if __name__ == "__main__":
    run_workout_app()