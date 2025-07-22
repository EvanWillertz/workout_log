# workout_log
This GUI app allows users to enter workouts and track progress over time.

## It allows you to:

1) Enter new exercises.
2) Create new workout blocks that hold templates of your weekly workouts so you can easily enter them. 
3) Create new wokrouts made from templates that hold the exercises for that particular wokrout. 
4) View all past workouts in each workout block.
5) View stats of all of your exercises and each rep range you've ever done. It also tracks total reps and volume.

## To use:

Download the exe program in the dist file and the corrisponding operating system. Start by entering your exercises and then building out workout blocks to add workouts to.


## If you make changes and wish to re-create the executable, plug this into your terminal with your current directory being this folder:

(**This is for Windows...**)
"pyinstaller --onefile --noconsole  --icon=barbell.ico --add-data "default_training_block_data.json;." --add-data "default_training_data.json;." --add-data "gym_pic.jpg;." --add-data "barbell.ico;." --distpath dist\Windows --workpath build --specpath build workout_app.py"