# workout_log
This GUI app allows users to enter workouts and track progress over time.

## It allows you to:

1) Enter new exercises.
2) Create new workout blocks that hold templates of your weekly workouts so you can easily enter them. 
3) Create new wokrouts made from templates that hold the exercises for that particular wokrout. 
4) View all past workouts in each workout block.
5) View stats of all of your exercises and each rep range you've ever done. It also tracks total reps and volume.

## To use:

Download the exe program in the release section in the repo that goes with the corrisponding operating system. Start by entering your exercises and then building out workout blocks to add workouts to. After you log workouts, you can then view them again in the view workouts area and visualize your progress in the view progress bar.


## If you make changes and wish to re-create the executable, plug this into your terminal with your current directory being this folder: This will recreate the executable in a clean way.

(**This is for Windows...** It lets you keep the barbell as the icon for the app.)
pyinstaller --onefile --noconsole  --icon=barbell.ico --add-data "default_training_block_data.json;." --add-data "default_training_data.json;." --add-data "gym_pic.jpg;." --add-data "barbell.ico;." --distpath dist\Windows --workpath build --specpath build workout_app.py

(**This is for Linux** If you use Linux, you have to go into workoutapp_gui.py and comment out / uncomment the code on lines 34-37.)
pyinstaller --onefile --noconsole --hidden-import=PIL._tkinter_finder --add-data "barbell-4.png:." --add-data "default_training_block_data.json:." --add-data "default_training_data.json:." --add-data "gym_pic.jpg:." --add-data "barbell.ico:." --distpath dist/Linux --workpath build --specpath build workout_app.py