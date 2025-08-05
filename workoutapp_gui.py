import customtkinter as ctk
from workout import Workout
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import matplotlib.dates as mdates
import sys
import os
import re




def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)




class WorkoutAppGUI(ctk.CTk):

    def __init__(self, manager):
        super().__init__()
        # get the manager and load the data stored there
        self.manager = manager

        # set title at top
        self.title("Workout Tracker")


        # This checks if it is using mac, if so, you have to use png for macOS or linux
        if sys.platform == "win32":
            self.iconbitmap(resource_path("barbell.ico"))
        elif sys.platform == "darwin":
            icon_img = Image.open(resource_path("barbell-4.png"))
            self.icon_image = ImageTk.PhotoImage(icon_img)
            self.iconphoto(False, self.icon_image)  # type: ignore
        elif sys.platform == "linux":
            icon_img = Image.open(resource_path("barbell-4.png"))
            icon_image = ImageTk.PhotoImage(icon_img)
            self.iconphoto(False, icon_image)   # type: ignore
            
        # set the geometry
        self.geometry("1100x700+200+100")  # width x height + x_offset + y_offset
        self.minsize(width=1100, height=700)
        self.configure(fg_color="#474747")   #90938F greenish   C0C0C0 blueish

        # Create container to hold all frames
        self.container = ctk.CTkFrame(self, fg_color="#474747")
        self.container.pack(fill="both", expand=True)
        # Let frames inside the container expand to fill space
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # ctk.set_appearance_mode("dark")

        # Create frames and keep references
        self.frames = {}
        for F in (NewBlockScreen, AddWorkoutScreen, HomeScreen, SeeStatesScreen, PastWorkoutsScreen, AllExercisesScreen):
            frame = F(self.container, self, self.manager)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the first screen
        self.show_frame(HomeScreen)

    def show_frame(self, frame_class):
        '''Raise the selected frame to the top.'''
        frame = self.frames[frame_class]

        # Call reset if available
        # for the NewWorkoutScreen, this first deletes any possible already exsisting frames and then creates the StartDate_NumberWorkouts frame
        if hasattr(frame, "reset"):
            frame.reset()

        frame.tkraise()



#############################################################################################################

########### This is the HomeScreen class which is the first screen the user sees when they open the app.

#############################################################################################################




class HomeScreen(ctk.CTkFrame):
    """Frame for the home screen with options to create a new block, add a workout, or view stats."""

    def __init__(self, parent, controller, manager):
        super().__init__(parent, fg_color="#474747")
        self.controller = controller
        self.manager = manager

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        # self.grid_propagate(False)  # Prevents the frame from resizing to fit its contents

        # loading the image for the home screen
        # self.original_image = Image.open('gym_pic.jpg')  # Make sure this image exists in the same directory
        self.original_image = Image.open(resource_path("gym_pic.jpg")) 
        self.ctk_image = ctk.CTkImage(light_image=self.original_image, dark_image=self.original_image, size=(500, 700))  # Resize as needed
    
        # Display the image in a label
        self.image_label = ctk.CTkLabel(self, image=self.ctk_image, text="")  # text="" hides label text
        self.image_label.grid(row=0, column=0, rowspan=6, sticky="nsw")


        self.label = ctk.CTkLabel(self, text="Welcome To Your Personal\nWorkout Tracker!", font=ctk.CTkFont(size=40, weight='bold'), text_color="#0C0C0C")
        self.label.grid(row=0, column=1, pady=(10, 0), sticky="n")

        # button to create a new training block
        self.new_block_button = ctk.CTkButton(self, border_color="#000000", border_width=2, hover_color="#28569C", text_color="#0C0C0C", fg_color="#2E63B3", width=550, height=80, font=ctk.CTkFont(size=35), text="Create Training Block", command=lambda: controller.show_frame(NewBlockScreen))
        self.new_block_button.grid(row=1, column=1, pady=(0, 10))

        # button to add a workout to an existing training block
        self.add_workout_button = ctk.CTkButton(self, border_color="#000000", border_width=2, hover_color="#28569C", text_color="#0C0C0C", fg_color="#2E63B3", width=550, height=80, font=ctk.CTkFont(size=35), text="Add Workout", command=lambda: controller.show_frame(AddWorkoutScreen))
        self.add_workout_button.grid(row=2, column=1, pady=10)

        # button to view stats of the training blocks
        self.view_stats_button = ctk.CTkButton(self, border_color="#000000", border_width=2, hover_color="#28569C", text_color="#0C0C0C", fg_color="#2E63B3", width=550, height=80, font=ctk.CTkFont(size=35), text="View Progress", command=lambda: controller.show_frame(SeeStatesScreen))
        self.view_stats_button.grid(row=3, column=1, pady=10)

        # button to view past workouts
        self.view_pastworkouts_button = ctk.CTkButton(self, border_color="#000000", border_width=2, hover_color="#28569C", text_color="#0C0C0C", fg_color="#2E63B3",  width=550, height=80, font=ctk.CTkFont(size=35), text="View Past Workouts", command=lambda: controller.show_frame(PastWorkoutsScreen))
        self.view_pastworkouts_button.grid(row=4, column=1, pady=10)

        # button to view all exercises
        self.view_exercises_button = ctk.CTkButton(self, border_color="#000000", border_width=2, hover_color="#28569C", text_color="#0C0C0C", fg_color="#2E63B3", width=550, height=80, font=ctk.CTkFont(size=35), text="View/Add Exercises", command=lambda: controller.show_frame(AllExercisesScreen))
        self.view_exercises_button.grid(row=5, column=1, pady=10)

        self.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        width = self.image_label.winfo_width()
        height = self.image_label.winfo_height()

        if width > 1 and height > 1:
            # Resize the original image
            resized_image = self.original_image.resize((width, height), Image.LANCZOS)

            # Create a NEW CTkImage from the resized image
            new_ctk_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image)

            # Update the image on the label
            self.image_label.configure(image=new_ctk_image)

            # Store a reference so it doesn't get garbage collected
            self.ctk_image = new_ctk_image




#############################################################################################################

########### This is the NewBlockScreen class which allows users to create a new training block.

#############################################################################################################








class NewBlockScreen(ctk.CTkFrame):
    """Frame for creating a new training block."""

    def __init__(self, parent, controller, manager):
        super().__init__(parent, fg_color="#474747")
        self.controller = controller
        self.manager = manager  # This will be what we manipulate to add blocks and workouts
        self.already_created = False  # This will be set to True when the user creates a block

        # self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure((0, 1), weight=1)

        # This is the blank frame to make the left frame fit exactly half the screen
        self.blank = ctk.CTkFrame(self, fg_color="transparent")
        self.blank.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.start_number = None  # we'll create this later

        self.exit_button = ctk.CTkButton(self, corner_radius=0, fg_color="#FF1E1E", hover_color="#CB1919", text="Exit to Home Screen (will not save block)", command=lambda: self.exit_to_home(), font=ctk.CTkFont(size=10), border_color="#000000", border_width=2, text_color="#0C0C0C")
        self.exit_button.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky='w')

    
    def exit_to_home(self):
        """Exits to the home screen without saving the block."""
        if self.already_created:
            self.manager.training_blocks.pop(-1)  # Remove the last block added
            self.manager.save_data()  # Save the changes to the data file

            self.already_created = False # Reset this so we know the block is no longer created

        self.controller.show_frame(HomeScreen)  # Show the home screen


    def create_block(self, start_date, num_workouts):
        """Creates a new training block and adds it to the manager."""

        # This gets called when the button inside StartDate_NumberWorkouts is clicked
        # print(f"Received in parent: {start_date}, {num_workouts}")

        # self.after(10, lambda:self.manager.add_training_block(start_date, num_workouts))
        self.manager.add_training_block(start_date, num_workouts)
        self.current_block = self.manager.training_blocks[-1]  # Get the most recently added block

        self.already_created = True  # Set this to True so we know the block has been created

        # creating multiple frames for each workout template
        self.frames = []
        self.curr_frame_idx = 0
        
        for i in range(int(num_workouts)):
            # Create a new BlocksWorkouts frame for each workout to collect the template information
            if i == int(num_workouts) - 1:
                workout_frame = BlocksWorkouts(self, self.manager, i + 1, last=True, on_submit_callback=self.add_template)
                workout_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

            else:
                workout_frame = BlocksWorkouts(self, self.manager, i + 1, last=False, on_submit_callback=self.add_template)
                workout_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

            self.frames.append(workout_frame)

        self.frames[0].tkraise()  # Show the first frame


    def show_next_frame(self):
        # goes to the next frame for the user to enter the workout template information
        # if we are on the last frame, then the program will go back to the home screen after the user clicks the submit button
        self.curr_frame_idx += 1
        if self.curr_frame_idx >= len(self.frames):
            self.already_created = False  # Reset this so we know the block is no longer created
            self.controller.show_frame(HomeScreen)
        else:
            self.frames[self.curr_frame_idx].tkraise()


    def add_template(self, template_name, exercises):
        """Adds a workout template to the current training block."""        

        self.manager.add_template_to_block(self.current_block, template_name, exercises)
        # self.manager.print_training_blocks()  # Print the current training blocks for debugging

        self.show_next_frame()  # Show the next frame for the next workout template


    def reset(self):
        # Destroy any existing workout frames
        if hasattr(self, "frames"):
            for frame in self.frames:
                frame.destroy()
        self.frames = []
        self.curr_frame_idx = 0
        self.current_block = None

        if self.start_number:
            self.start_number.destroy()

        # this creates the StartDate_NumberWorkouts frame after the reset so that it is blank 
        # This calls the create_block method when the button is clicked to return the start date and number of workouts
        self.start_number = StartDate_NumberWorkouts(self, on_submit_callback=self.create_block) 
        self.start_number.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="wsne")




class BlocksWorkouts(ctk.CTkFrame):
    """This block is called as many times as there are workout templates needed for the training block.
        It will have the workout of the week number, an entry box for the workout name, and a scrollable frame
        for the exercises with checkboxes to select the exercises for that workout."""
    
    def __init__(self, parent, manager, workout_num, last=False, on_submit_callback=None, ):
        super().__init__(parent)
        self.on_submit_callback = on_submit_callback
        self.poss_exercises = manager.all_exercises  # This will be a list of all the exercises in the manager
 
        self.grid_rowconfigure(0, weight=0)  # title
        self.grid_rowconfigure(1, weight=0)  # name:
        self.grid_rowconfigure(2, weight=0)  # Entry
        self.grid_rowconfigure(3, weight=0)  # Label
        self.grid_rowconfigure(4, weight=1)  # ScrollableFrame takes remaining space
        self.grid_rowconfigure(5, weight=0)  # Button
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.configure(fg_color="#3E505F", border_color="#000000", border_width=2.5)  # Set the background color of the frame   7E8D9C    C0C0C0


        # for the title of the workout
        self.title_label = ctk.CTkLabel(self, text_color="#0C0C0C", text=f"Training Block Workout {workout_num}", font=ctk.CTkFont(size=35, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # for the workout name entry
        self.label = ctk.CTkLabel(self, text="Workout Name:", font=ctk.CTkFont(size=30, weight="bold"), text_color="#0C0C0C")
        self.label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="wes")
        self.workout_name = ctk.CTkEntry(self, font=ctk.CTkFont(size=30), border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#2C2C2C", placeholder_text_color="#0C0C0C", justify="center")
        self.workout_name.grid(row=2, column=0, padx=100, pady=(10, 0), sticky="new")

        # for the exercises label and scrollable frame fro users to select exercises
        self.label = ctk.CTkLabel(self, text="Exercises:", text_color="#0C0C0C", font=ctk.CTkFont(size=30, weight="bold"))
        self.label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="wes")
        self.exercise_scrollframe = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#90938F", border_color="#2C2C2C")
        self.exercise_scrollframe.grid(row=4, column=0, padx=10, pady=(10, 10), sticky="nsew")
        
        # self.exercise_scrollframe.grid_columnconfigure(0, weight=1)  # Empty space on the left
        # self.exercise_scrollframe.grid_columnconfigure(1, weight=0)  # First checkbox column
        # self.exercise_scrollframe.grid_columnconfigure(2, weight=0)  # Second checkbox column
        # self.exercise_scrollframe.grid_columnconfigure(3, weight=1)  # Empty space on the right


        # Create checkboxes for each exercise in the workout manager (all of them)
        self.selected_exercises = {}  # Dictionary to hold the selected exercises
        # double sided checkboxes for the exercises
        for i, exercise in enumerate(self.poss_exercises):
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(self.exercise_scrollframe, text=exercise, font=ctk.CTkFont(size=15, weight="bold"), variable=var, text_color="#0C0C0C", border_color="#2C2C2C", hover_color="#298031", fg_color="#298031")

            # Calculate the row and column for two columns
            row = i // 2
            column = i % 2
            # column = 1 if i % 2 == 0 else 2  # Use columns 1 and 2 for centered layout

            checkbox.grid(row=row, column=column, padx=10, pady=2, sticky="w")
            self.selected_exercises[exercise] = var


        if last:
            self.button = ctk.CTkButton(self, text="Submit Training Block", command=self.get_entries, fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), corner_radius=20)
            self.button.grid(row=5, column=0, padx=10, pady=(10, 10))
        else:
            self.button = ctk.CTkButton(self, text="Enter", command=self.get_entries, fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), corner_radius=20)
            self.button.grid(row=5, column=0, padx=10, pady=(10, 10))


    def get_entries(self):
        """Returns the name and the exercises of the template to make."""
        selected = [exercise for exercise, var in self.selected_exercises.items() if var.get()]

        if self.on_submit_callback:
            self.on_submit_callback(self.workout_name.get(), selected)


class StartDate_NumberWorkouts(ctk.CTkFrame):
    """Frame for entering the starting date and number of workouts per week."""

    def __init__(self, parent, on_submit_callback=None):
        super().__init__(parent)
        self.on_submit_callback = on_submit_callback
        self.reset()

    def create_widgets_from_scratch(self, on_submit_callback=None):
        self.on_submit_callback = on_submit_callback

        self.grid_rowconfigure((0, 1, 2 ,3, 4, 5), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.configure(fg_color="#3E505F", border_color="#000000", border_width=2.5)  # Set the background color of the frame   7E8D9C    C0C0C0


        self.title_label = ctk.CTkLabel(self, text_color="#0C0C0C", text=f"Create Your Training Block:", font=ctk.CTkFont(size=35, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="we")

        self.label = ctk.CTkLabel(self, text_color="#0C0C0C", text="Start Date (MM-DD-YYYY):", font=ctk.CTkFont(size=30, weight="bold"))
        self.label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="wes")

        self.entry_start_date = ctk.CTkEntry(self, border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#2C2C2C", font=ctk.CTkFont(size=30), placeholder_text="MM-DD-YYYY", placeholder_text_color="#0C0C0C", justify="center")
        self.entry_start_date.grid(row=2, column=0, padx=100, pady=(10, 0), sticky="new")

        self.label = ctk.CTkLabel(self, text_color="#0C0C0C", text="Number of Workouts Per Week:", font=ctk.CTkFont(size=30, weight="bold"))
        self.label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="wes")

        self.entry_number_workouts = ctk.CTkEntry(self, border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#2C2C2C", placeholder_text_color="#0C0C0C", font=ctk.CTkFont(size=30), placeholder_text="1, 2, 3... etc", justify="center")
        self.entry_number_workouts.grid(row=4, column=0, padx=100, pady=(10, 0), sticky="new")

        self.enter_button = ctk.CTkButton(self, border_width=2, border_color="#2C2C2C", corner_radius=20, text="Enter", hover_color="#1F6326", text_color="#0C0C0C", fg_color="#298031", command=self.get_entries, font=ctk.CTkFont(size=30, weight="bold"))
        self.enter_button.grid(row=5, column=0, padx=10, pady=(10, 0))

    def get_entries(self):
        """Returns the start date and number of workouts per week."""

        start_date = self.entry_start_date.get()
        num_workouts = self.entry_number_workouts.get()

        if num_workouts.isdigit() and re.match(r"\d\d-\d\d-\d\d\d\d", start_date):
            if self.on_submit_callback:
                self.enter_button.configure(state="disabled")  # Lock the button
                self.entry_start_date.configure(state="disabled")  # Lock the entry
                self.entry_number_workouts.configure(state="disabled")  # Lock the entry
                # self.after(50, lambda: self.enter_button.configure(state="disabled"))
                # self.after(50, lambda: self.entry_start_date.configure(state="disabled"))
                # self.after(50, lambda: self.entry_number_workouts.configure(state="disabled"))

                self.on_submit_callback(start_date, num_workouts)
        else:
            print("Invalid input. Please enter a valid start date and number of workouts.")

    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_widgets_from_scratch(self.on_submit_callback)









#############################################################################################################

########### This is the AddWorkoutScreen class which allows users to add a workout to an existing training block.

#############################################################################################################








class AddWorkoutScreen(ctk.CTkFrame):
    """Frame for adding a workout to an existing training block."""

    def __init__(self, parent, controller, manager):
        super().__init__(parent, fg_color="#474747")
        self.controller = controller
        self.manager = manager  # This will be what we manipulate to add blocks and workouts
        self.already_created = False # if a workout is already in the middle of being created when the back button is hit, then delete the workout
        self.workout_entries = {} # this will be added to the workout object at the end

        # self.workout = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_propagate(False)  # Prevents the frame from resizing to fit its contents

        # filler so that the first frame doesn't spill over the half way mark
        self.blank = ctk.CTkFrame(self, fg_color="transparent")
        self.blank.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

        self.block_template = None # this will be created in the reset method

        self.exit_button = ctk.CTkButton(self, corner_radius=0, fg_color="#FF1E1E", hover_color="#CB1919", text="Exit to Home Screen (will not save Workout)", command=lambda: self.exit_to_home(), font=ctk.CTkFont(size=10), border_color="#000000", border_width=2, text_color="#0C0C0C")
        self.exit_button.grid(row=1, column=0, padx=(0, 10), pady=(0, 0), sticky='w')

        # self.diff_date = ctk.CTkEntry(self, placeholder_text="Enter Workout Date, If Not Today (MM-DD-YYYY)", fg_color="#90938F", border_color="#000000", border_width=2, font=ctk.CTkFont(size=20), placeholder_text_color="#0C0C0C", justify="center", text_color="#0C0C0C")
        # self.diff_date.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")
        

    def exit_to_home(self):
        """Exits to the home screen without saving the block."""

        self.controller.show_frame(HomeScreen)  # Show the home screen

    
    def reset(self):
        # Destroy any existing workout frames
        if hasattr(self, "frames"):
            for frame in self.frames:
                frame.destroy()
        self.frames = []
        self.curr_frame_idx = 0
        self.current_block = None

        if self.block_template:
            self.block_template.destroy()

        self.diff_date = ctk.CTkEntry(self, placeholder_text="Enter Workout Date, If Not Today (MM-DD-YYYY)", fg_color="#90938F", border_color="#000000", border_width=2, font=ctk.CTkFont(size=20), placeholder_text_color="#0C0C0C", justify="center", text_color="#0C0C0C")
        self.diff_date.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        # this creates the StartDate_NumberWorkouts frame after the reset so that it is blank 
        # This calls the create_block method when the button is clicked to return the start date and number of workouts
        self.block_template = PickBlock_PickTemplate(self, self.controller, on_submit_callback=self.create_workout)
        self.block_template.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="wsne")


    def create_workout(self, block, template):
        # print(f"creating workout now with block starting on {block.starting_date} with template {template.name}")
        # Destroy existing exercise frames if any
        if hasattr(self, "frames"):
            for frame in self.frames:
                frame.destroy()

        # initializing the workout object
        self.workout = Workout(template_name=template.name)
        self.block = block

        self.frames = []
        self.curr_frame_idx = 0

        for i in range(len(template.exercises)):
            if i == len(template.exercises) - 1:

                exercise_frame = Exercises(self, template.exercises[i], last=True, on_submit_callback=self.add_entry)
                exercise_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="wsne")
                # if is last workout
            else:
                exercise_frame = Exercises(self, template.exercises[i], last=False, on_submit_callback=self.add_entry)
                exercise_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="wsne")

            self.frames.append(exercise_frame)
        
        self.frames[0].tkraise()


    def add_entry(self, exercise_name, reps, weights, skip, last, want_new_exercise):
        # print(exercise_name)
        # print(reps)
        # print(weights)
        # print(skip)
        # print(last)
        # print(want_new_exercise)

        if want_new_exercise:
            new_exercise_frame = Exercises(self, "None", last=True, on_submit_callback=self.add_entry, new_exercise=True)
            new_exercise_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="wsne")
            self.frames.append(new_exercise_frame)

        if not skip:
            entry_list = []
            for num_reps, weight in zip(reps, weights):
                entry_list.append([num_reps, weight])

            # print(entry_list)

            self.workout_entries[exercise_name] = entry_list
            
        if last:
            if self.diff_date.get() != "":
                # if the user entered a different date, then we will use that date instead of today
                
                # Convert to datetime object
                date_obj = datetime.strptime(self.diff_date.get(), "%m-%d-%Y")

                # Format as "Month day, year"
                formatted_date = date_obj.strftime("%B %d, %Y")
                self.workout.date = formatted_date

                # self.diff_date.setvar("")  # Reset the date entry field
                self.diff_date.delete(0, 'end')  # Clear the date entry field

            self.workout.add_entry(self.workout_entries) # adding the entries list to the workout object
            self.block.add_workout(self.workout)

            self.manager.save_data()
            self.manager.add_workout_to_tracker(self.workout) # adds the information in the wokrout to the tracker to keep track of stats...

        self.show_next_frame()


    def show_next_frame(self):
        # goes to the next frame for the user to enter the info for the next exerise
        # if we are on the last frame, then the program will go back to the home screen after the user clicks the submit button
        self.curr_frame_idx += 1
        if self.curr_frame_idx >= len(self.frames):
            # self.already_created = False  # Reset this so we know the block is no longer created

            self.workout_entries = {}  ### Trying to fix bug of the workout entries carrying over to the next workout ###

            self.controller.show_frame(HomeScreen)
        else:
            self.frames[self.curr_frame_idx].tkraise()
            


class Exercises(ctk.CTkFrame):
    """ There is going to be one of these for each of the exercises in the template. They
    will be stacked and shown one at a time. This is where the user will enter the number 
    of sets, reps, and weight for each of the exercises they did that day!"""

    def __init__(self, parent, exercise_name, last=False, on_submit_callback=None, new_exercise=False):
        super().__init__(parent)
        self.on_submit_callback = on_submit_callback
        self.exercise_name = exercise_name
        self.last = last
        self.want_new_exercise = False

        self.configure(fg_color="#3E505F", border_color="#000000", border_width=2.5)  # Set the background color of the frame   7E8D9C    C0C0C0

        self.num_sets_val = None
        self.num_reps = []
        self.weight = []
        self.did_skip = False

        if not new_exercise:
            self.grid_rowconfigure(0, weight=0) # name of exercise
            self.grid_rowconfigure(1, weight=0) # number of sets
            self.grid_rowconfigure(2, weight=0) # number of sets button submit
            self.grid_rowconfigure(3, weight=1) # two columns for reps and weight for each set
            self.grid_rowconfigure(4, weight=0) # two buttons for skipping exercise and replacing

            self.grid_columnconfigure((0, 1), weight=1)

            self.grid_propagate(False)

            self.label = ctk.CTkLabel(self, text_color="#0C0C0C", text=f"{exercise_name}", font=ctk.CTkFont(size=25, weight="bold"))
            self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

            self.skip_var = ctk.BooleanVar()
            self.skip_exercise_check = ctk.CTkCheckBox(self, text="Skip Exercise", variable=self.skip_var, text_color="#0C0C0C", font=ctk.CTkFont(size=25), fg_color="#298031", hover_color="#1F6326")
            self.skip_exercise_check.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ns")

            self.label = ctk.CTkLabel(self, text="Number of sets   =", text_color="#0C0C0C", font=ctk.CTkFont(size=25, weight="bold"))
            self.label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

            self.num_sets = ctk.CTkEntry(self, border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#2C2C2C", placeholder_text_color="#0C0C0C", font=ctk.CTkFont(size=30), justify="center")
            self.num_sets.grid(row=1, column=1, padx=0, pady=10, sticky="w")
            self.num_sets_button = ctk.CTkButton(self, text="Enter Set Number", command=self.get_reps_weight, text_color="#0C0C0C", font=ctk.CTkFont(size=25, weight="bold"), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", corner_radius=20)
            self.num_sets_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            if last:
                self.submit_button = ctk.CTkButton(self, text="Submit Workout", command=self.submit_exercise, text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", corner_radius=20)
                self.submit_button.grid(row=4, column=0, pady=10)
                # this is for when you want to add another exercise that is not usually in the template workout
                self.submit_button = ctk.CTkButton(self, text="Enter & Add New Exercise", command=self.create_new_exercise, text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", corner_radius=20)
                self.submit_button.grid(row=4, column=1, pady=10)
            else:
                self.submit_button = ctk.CTkButton(self, text="Enter Exercise", command=self.submit_exercise, text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", corner_radius=20)
                self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        else: # this is a different configuration of the exercise frame so that the user can enter a new exercise
            self.grid_rowconfigure(0, weight=1) # picking exercise
            self.grid_rowconfigure(1, weight=0) # entering number of sets
            self.grid_rowconfigure(2, weight=0) # button for submitting number of sents
            self.grid_rowconfigure(3, weight=1) # reps and weight for each set scroll bars
            self.grid_rowconfigure(4, weight=0) # buttons for exit or enter another exercise

            self.grid_columnconfigure((0, 1), weight=1)
            self.grid_propagate(False)

            self.skip_var = ctk.BooleanVar(value=False) # because the object needs this attribute for some functions
            self.new_exercise = ctk.StringVar(value=None)

            # first row
            self.label = ctk.CTkLabel(self, text=f"Select Exercise: ", font=ctk.CTkFont(size=25, weight="bold"), text_color="#0C0C0C")
            self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

            self.exercise_scrollable = ctk.CTkScrollableFrame(self, height=50, border_width=2, fg_color="#90938F", border_color="#2C2C2C")
            self.exercise_scrollable.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew")

            # populate exercise scrollable
            all_exercises = parent.manager.all_exercises
            for i in range(len(all_exercises)):
                self.exercise_button = ctk.CTkRadioButton(self.exercise_scrollable, text=f"{all_exercises[i]}", variable=self.new_exercise, value=all_exercises[i],
                                         command=lambda e=all_exercises[i]: self.add_new_exercise(e), font=ctk.CTkFont(size=15), text_color="#0C0C0C", fg_color="#298031", hover_color="#1F6326", border_color="#2C2C2C")
                self.exercise_button.grid(row=i, column=0, padx=5, pady=5, sticky='ew')

            # second row
            self.label = ctk.CTkLabel(self, text="Number of sets   =", text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"))
            self.label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

            self.num_sets = ctk.CTkEntry(self, border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#2C2C2C", placeholder_text_color="#0C0C0C", font=ctk.CTkFont(size=30), justify="center")
            self.num_sets.grid(row=1, column=1, padx=0, pady=10, sticky="w")
            # third row
            self.num_sets_button = ctk.CTkButton(self, text="Enter Set Number", command=self.get_reps_weight, text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", corner_radius=20)
            self.num_sets_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            # fourth row (reps and weight function)

            # fifth row
            self.submit_button = ctk.CTkButton(self, text="Submit Workout", command=self.submit_exercise, text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", corner_radius=20)
            self.submit_button.grid(row=4, column=0, pady=10)
            # this is for when you want to add another exercise that is not usually in the template workout
            self.submit_button = ctk.CTkButton(self, text="Enter & Add New Exercise", command=self.create_new_exercise, text_color="#0C0C0C", font=ctk.CTkFont(size=20, weight="bold"), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#2C2C2C", corner_radius=20)
            self.submit_button.grid(row=4, column=1, pady=10)


    def submit_exercise(self):
        if self.skip_var.get() or self.num_sets.get() == "":
            # print("Is skipping")
            self.did_skip = True
            reps = []
            weights = []
        else:
            reps, weights = self.collect_data()
        
        
        if self.on_submit_callback:
            self.on_submit_callback(self.exercise_name, reps, weights, self.did_skip, self.last, self.want_new_exercise)

    
    def create_new_exercise(self):
        """When the user hits "Enter & Add New Exercise" button, it sends them here which creates a
            new Exercise frame that is a little different layout. This then calls submit_exercise()
            with the last exercise's information and the the new frame to be added to he frame list."""
        
        self.want_new_exercise = True  # so that a new Exercise object is made
        self.last = False # this would normally be true because it was the last exercise until the user 
                            # clicked the add new exercise button
        self.submit_exercise()  # submits the current exercise normally
        

    def add_new_exercise(self, exercise):
        """To get the name of the Exercise from the radio button scrollable thing..."""
        self.exercise_name = exercise
        

        

    def get_reps_weight(self):

        if hasattr(self, "reps_entries"):
            for widget in self.reps_scroll.winfo_children():
                widget.destroy()
            for widget in self.weight_scroll.winfo_children():
                widget.destroy()

        # Get number of sets
        try:
            self.num_sets_val = int(self.num_sets.get())
        except ValueError:
            print("Invalid number of sets.")
            return

        self.reps_scroll = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#90938F", border_color="#2C2C2C")
        self.reps_scroll.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

        self.weight_scroll = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#90938F", border_color="#2C2C2C")
        self.weight_scroll.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        self.reps_entries = []
        self.weight_entries = []


        for i in range(int(self.num_sets_val)):
            # reps
            reps_label = ctk.CTkLabel(self.reps_scroll, text=f"Set {i+1} Reps:", font=ctk.CTkFont(size=25), text_color="#0C0C0C")
            reps_label.grid(row=i, column=0, padx=5, pady=5, sticky='e')

            reps_entry = ctk.CTkEntry(self.reps_scroll, width=60, font=ctk.CTkFont(size=25), border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#2C2C2C", justify="center")
            reps_entry.grid(row=i, column=1, pady=5, sticky='w')
            self.reps_entries.append(reps_entry)

            # Weight
            weight_label = ctk.CTkLabel(self.weight_scroll, text=f"Set {i+1} Weight:", font=ctk.CTkFont(size=25), text_color="#0C0C0C")
            weight_label.grid(row=i, column=0, padx=5, pady=5, sticky='e')

            weight_entry = ctk.CTkEntry(self.weight_scroll, width=60, font=ctk.CTkFont(size=25), border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#2C2C2C", justify="center")
            weight_entry.grid(row=i, column=1, padx=(5, 50), pady=5, sticky='w')
            self.weight_entries.append(weight_entry)

    def collect_data(self):
        reps_list = [int(entry.get()) for entry in self.reps_entries]
        weight_list = [int(entry.get()) for entry in self.weight_entries]
        return reps_list, weight_list





class PickBlock_PickTemplate(ctk.CTkFrame):
    """Frame for picking a workout template from the selected training block."""
    def __init__(self, parent, controller, on_submit_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.on_submit_callback = on_submit_callback
        self.manager = controller.manager  # Access the manager from the controller

        self.configure(fg_color="#3E505F", border_color="#000000", border_width=2.5)  # Set the background color of the frame   7E8D9C    C0C0C0

        # these are the actual variables I will pass on...
        self.choosen_block = None
        self.choosen_template = None

        # these are the variables to be grabbed from the radio buttons
        # these only matter for the buttons... not actuall variable to use
        self.block = ctk.StringVar(value=None)
        self.template = ctk.StringVar(value=None)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)  # Prevents the frame from resizing to fit its contents

        self.label = ctk.CTkLabel(self, text="Select a Training Block:", font=ctk.CTkFont(size=30), text_color="#0C0C0C")
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="we")

        self.block_scrollframe = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#90938F", border_color="#2C2C2C")
        self.block_scrollframe.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nsew")

        # Populate the scrollable frame with training blocks
        for block in self.manager.training_blocks:
            block_button = ctk.CTkRadioButton(self.block_scrollframe, text=block.starting_date, variable=self.block, value=block,
                                         command=lambda b=block: self.pick_template(b), font=ctk.CTkFont(size=30), text_color="#0C0C0C", border_color="#2C2C2C", hover_color="#298031", fg_color="#298031")
            block_button.pack(fill="x", padx=10, pady=2)


        self.label_template = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=15))
        self.label_template.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="we")
        self.template_scrollframe = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.template_scrollframe.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="nsew")


    def get_block_template(self, block, template):
        """Returns the start date and number of workouts per week."""

        if self.on_submit_callback:
            self.on_submit_callback(block, template)


    def pick_template(self, block):
        """Picks a workout template from the selected training block."""

        self.choosen_block = block
        
        self.label = ctk.CTkLabel(self, text=f"Select a Workout Template from\n Block starting on {block.starting_date}:", font=ctk.CTkFont(size=30), text_color="#0C0C0C")
        self.label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="we")
        self.template_scrollframe.configure(border_width=2, fg_color="#90938F", border_color="#2C2C2C")


        for widget in self.template_scrollframe.winfo_children():
            widget.destroy()

        # Populate the scrollable frame with templates from the selected block
        for idx, template in enumerate(block.templates):
            template_button = ctk.CTkRadioButton(self.template_scrollframe, text=f"{idx + 1}. {template.name}", variable=self.template, value=template,
                                           command=lambda t=template: self.get_block_template(self.choosen_block, t), text_color="#0C0C0C", font=ctk.CTkFont(size=15), border_color="#2C2C2C", hover_color="#298031", fg_color="#298031")
            template_button.pack(fill="x", padx=10, pady=2)
        








#############################################################################################################

########### This is the SeeStatesScreen class which allows users to view stats of themselves

#############################################################################################################










class SeeStatesScreen(ctk.CTkFrame):
    """Frame for viewing stats of the training blocks."""

    def __init__(self, parent, controller, manager):
        super().__init__(parent, fg_color="#474747")
        self.controller = controller
        self.manager = manager


    def initialize_setup(self):
        self.fig = None
        self.canvas = None

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_propagate(False)  # Prevents the frame from resizing to fit its

        # Create widgets for the stats screen
        self.label = ctk.CTkLabel(self, text="Vizualize Your Progress!", font=ctk.CTkFont(size=25, weight="bold"), text_color="#0C0C0C")
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ew')

        total_data = self.manager.over_time_tracker.get("Stats", None)
        self.total_labels = ctk.CTkLabel(self, text=f"Total Number of Reps = {total_data['Total Rep #']}, Total Weight Lifted = {total_data['Total Volume']} lbs", font=ctk.CTkFont(size=20), text_color="#0C0C0C")
        self.total_labels.grid(row=0, column=1, padx=10, pady=(10, 0), sticky='ew')


        self.exercise = ctk.StringVar(value=None)

        # the scroll frame for the user to pick the exercise to see stats from
        self.pick_exercise = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#3E505F", border_color="#000000")
        self.pick_exercise.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        label = ctk.CTkLabel(self.pick_exercise, text="Pick an exercise:", font=ctk.CTkFont(size=15), text_color="#0C0C0C")
        label.pack(padx=10, pady=10)

        # this is to see the volume over time for all workouts
        self.exercise_option = ctk.CTkRadioButton(self.pick_exercise, text="Over Time Progress", text_color='orange', variable=self.exercise, value="Over Time Progress",
                                         command=lambda e="Over Time Progress": self.choose_exercise(e), font=ctk.CTkFont(size=20))
        self.exercise_option.pack(fill="x", padx=10, pady=(2, 20))

        for exercise in self.manager.all_exercises:
            self.exercise_option = ctk.CTkRadioButton(self.pick_exercise, text=exercise, variable=self.exercise, value=exercise,
                                         command=lambda e=exercise: self.choose_exercise(e), font=ctk.CTkFont(size=20), text_color="#0C0C0C", fg_color="#298031", hover_color="#1F6326", border_color="#2C2C2C")
            self.exercise_option.pack(fill="x", padx=10, pady=2)


        self.scroll_frame = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#3E505F", border_color="#000000")
        self.scroll_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure((0, 1), weight=1)  # make two columns

        self.canvases = []  # Store canvas references for cleanup if needed

        # Button to go back to the main screen
        self.back_button = ctk.CTkButton(self, corner_radius=0, fg_color="#FF1E1E", hover_color="#CB1919", text="Exit to Home Screen", command=lambda: self.go_back_to_main(), font=ctk.CTkFont(size=10), border_color="#000000", border_width=2, text_color="#0C0C0C")
        self.back_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='')

        self.max_label = ctk.CTkLabel(self, text=f"")
        self.max_label.grid(row=2, column=1, padx=10, pady=(0, 10), sticky='ew')


    def choose_exercise(self, e):

        if self.canvases != []:
            self.delete_graphs()  # Clean up any existing graphs

        self.show_exercise_data(e)

    
    def show_exercise_data(self, exercise):
        # print(f"Showing stats for exercise: {exercise}")

        if exercise != "Over Time Progress":
            # display label for the max of the exercise
            max = self.manager.over_time_tracker['Personal Bests'][exercise]
            self.max_label = ctk.CTkLabel(self, text=f"Your PB for {exercise} is {max[1]} lbs, completed for {max[0]} reps on {max[2]}!", font=ctk.CTkFont(size=20), text_color="#0C0C0C")
            self.max_label.grid(row=2, column=1, padx=10, pady=(0, 10), sticky='ew')


            raw_exercise_data = self.manager.over_time_tracker.get(exercise, None)

            # this orders the data by number of reps so that the smaller number of reps is first
            # Separate out 'volume' first
            volume_item = ("Volume", raw_exercise_data["Volume"])

            # Sort remaining items by int-converted keys
            other_items = sorted(
                ((k, v) for k, v in raw_exercise_data.items() if k != "Volume"),
                key=lambda item: int(item[0])
            )

            # Combine them
            exercise_data = dict([volume_item] + other_items)


            # this creates the number of graphs based on the different rep numbers found for the excersise
            for i, rep_num in enumerate(exercise_data.keys()):  
                
                # Convert to datetime objects
                dates = [datetime.strptime(date, "%B %d, %Y") for date in exercise_data[rep_num][1]]
                weights = exercise_data[rep_num][0]

                fig, ax = plt.subplots(figsize=(6, 4.1))
                ax.plot(dates, weights, marker='o')

                if rep_num == "Volume":
                    ax.set_title(f"{exercise} Volume Progress", fontsize=14)
                    ax.set_ylabel("Volume Per Workout (lbs)")
                    ax.set_xlabel("Date")
                else:
                    ax.set_title(f"{exercise} Progress for {rep_num} Reps", fontsize=14)
                    ax.set_ylabel("Weight (lbs)")
                    ax.set_xlabel("Date")

                # this formats the dates for the x-axis
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))  # e.g., "Jun 23"
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                ax.grid(True)  # Add grid for better readability
                fig.autofmt_xdate()  # Auto-rotate date labels

                canvas = FigureCanvasTkAgg(fig, master=self.scroll_frame)
                canvas.draw()
                
                # Double-column logic
                row = i // 2
                col = i % 2
                canvas.get_tk_widget().grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                self.canvases.append((canvas, fig))  # Store for later cleanup
            
        else: # this is for plotting the over time total metrics (volume and rep numbers)
            
            # this will make the display dissapear if another exercise is choosen before this option
            self.max_label = ctk.CTkLabel(self, text=f"")
            self.max_label.grid(row=2, column=1, padx=10, pady=(0, 10), sticky='ew')

            for i, metric in enumerate(['Volume Per Workout', 'Rep # Per Workout']):

                stats = self.manager.over_time_tracker['Stats']
                dates = [datetime.strptime(date, "%B %d, %Y") for date in stats[metric][1]]
                volumes = stats[metric][0]

                fig, ax = plt.subplots(figsize=(6, 4.1))
                ax.plot(dates, volumes, marker='o')
                ax.set_title(f"Total {metric} Over Time", fontsize=14)
                ax.set_ylabel(f"{metric} (lbs)")
                ax.set_xlabel("Date")
                ax.grid(True)

                # this formats the dates for the x-axis
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %y"))  # e.g., "Jun 23"
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                fig.autofmt_xdate()  # Auto-rotate date labels

                canvas = FigureCanvasTkAgg(fig, master=self.scroll_frame)
                canvas.draw()

                canvas.get_tk_widget().grid(row=i, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
                self.canvases.append((canvas, fig))
    

    def delete_graphs(self):

        for canvas, fig in self.canvases:
            canvas.get_tk_widget().destroy()
            plt.close(fig)


    def go_back_to_main(self):
        """Goes back to the main screen."""
        self.delete_graphs()  # Clean up any existing graphs
        self.controller.show_frame(HomeScreen)

    
    def reset(self):

        self.initialize_setup()




#############################################################################################################

########### This is the AllExercisesScreen class which allows users to view and add exercises to their workout log.

#############################################################################################################





class PastWorkoutsScreen(ctk.CTkFrame):
    """This will allow users to view past workouts that were submitted in their different training blocks."""

    def __init__(self, parent, controller, manager):
        super().__init__(parent, fg_color="#474747")
        self.controller = controller
        self.manager = manager

    def initialize_setup(self):

        self.block = ctk.StringVar(value=None)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text="Explore Past Workouts!", font=ctk.CTkFont(size=35), text_color="#0C0C0C")
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0))

        # the scroll frame for the user to pick the block to see past workouts from
        self.pick_block = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#3E505F", border_color="#000000")
        self.pick_block.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        label = ctk.CTkLabel(self.pick_block, text="Pick a Training Block:", font=ctk.CTkFont(size=19), text_color="#0C0C0C")
        label.pack(padx=10, pady=10)

        for block in self.manager.training_blocks:
            self.block_option = ctk.CTkRadioButton(self.pick_block, text=block.starting_date, variable=self.block, value=block,
                                         command=lambda b=block: self.choose_block(b), font=ctk.CTkFont(size=30), text_color="#0C0C0C")
            self.block_option.pack(fill="x", padx=10, pady=2)


        # this is going to be the text box that the user can see all the past workouts from
        # the training block they chose
        self.words = ctk.CTkTextbox(self, wrap="word", font=ctk.CTkFont(size=25), text_color="#0C0C0C", border_width=2, fg_color="#90938F", border_color="#000000")
        self.words.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")


        # Button to go back to the main screen
        self.back_button = ctk.CTkButton(self, corner_radius=0, fg_color="#FF1E1E", hover_color="#CB1919", text="Exit to Home Screen", command=lambda: self.go_back_to_main(), font=ctk.CTkFont(size=10), border_color="#000000", border_width=2, text_color="#0C0C0C")
        self.back_button.grid(row=2, column=0, padx=10, pady=(0, 10))


    def choose_block(self, b):
        self.display_workouts(b)

    
    def display_workouts(self, block):
        self.words.delete("1.0", "end")

        # fill the text box with the exercises:
        for workout in block.workouts:
            self.words.insert("end", self.format_workout_table(workout) + "\n")
        

    def format_workout_table(self, workout):
        lines = [f"{workout.date} — Workout: {workout.template_name}\n"]

        for name, sets in workout.entries.items():
            lines.append(f"{name}")
            for reps, weight in sets:
                lines.append(f"       - {reps} x {int(weight)} lbs")
            lines.append("")  # Blank line between exercises

        lines.append("-" * 100)  # Separator line

        return "\n".join(lines)

    def clear_content(self):
        self.words.delete("1.0", "end")

    def go_back_to_main(self):
        self.clear_content()
        self.controller.show_frame(HomeScreen)

    def reset(self):

        self.initialize_setup()





#############################################################################################################

########### This is the AllExercisesScreen class which allows users to view and add exercises to their workout log.

#############################################################################################################




class AllExercisesScreen(ctk.CTkFrame):
    """Frame for viewing all exercises."""

    def __init__(self, parent, controller, manager):
        super().__init__(parent, fg_color="#474747")
        self.controller = controller
        self.manager = manager

        # Set up the frame layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_propagate(False)

        # Create widgets for the all exercises screen
        self.label = ctk.CTkLabel(self, text="All Exercises", font=ctk.CTkFont(size=40), text_color="#0C0C0C")
        self.label.grid(row=0, column=1, pady=20, sticky="n")

        # Create a scrollable frame to display all exercises
        self.exercise_scrollframe = ctk.CTkScrollableFrame(self, border_width=2, fg_color="#3E505F", border_color="#000000")
        self.exercise_scrollframe.grid(row=0, column=0, rowspan=3, padx=10, pady=(10, 10), sticky="nsew")

        # Populate the scrollable frame with checkboxes for each exercise
        for exercise in self.manager.all_exercises:  # Load exercises from the manager
            label = ctk.CTkLabel(self.exercise_scrollframe, text=f"- {exercise}", anchor="w", font=ctk.CTkFont(size=25), text_color="#0C0C0C")
            label.grid(sticky="w", padx=10, pady=2)

        # self.box = ctk.CTkComboBox(self, font=ctk.CTkFont(size=25), fg_color="#90938F", text_color="#0C0C0C", border_color="#000000")
        # self.box.grid(row=1, rowspan=3, column=1, padx=10, pady=(10, 10), sticky="ew")

        self.box = ctk.CTkFrame(self, fg_color="#3E505F", border_color="#000000", border_width=2)
        self.box.grid(row=1, column=1, padx=25, pady=(25, 25), sticky="ew")
        self.box.grid_rowconfigure(0, weight=1)
        self.box.grid_rowconfigure(1, weight=1)
        self.box.grid_rowconfigure(2, weight=1)
        self.box.grid_columnconfigure(0, weight=1)


        # Add a label for adding new exercises
        self.label = ctk.CTkLabel(self.box, text="Add New Exercise:", font=ctk.CTkFont(size=30), text_color="#0C0C0C")
        self.label.grid(row=0, column=0, pady=(10, 10))
        # Entry for new exercise name
        self.new_exercise_entry = ctk.CTkEntry(self.box, placeholder_text="Enter new exercise name...", placeholder_text_color="#0C0C0C", font=ctk.CTkFont(size=25), border_width=2, fg_color="#90938F", text_color="#0C0C0C", border_color="#000000", width=400, justify="center")
        self.new_exercise_entry.grid(row=1, column=0, padx=10, pady=(10, 10))

        # Button to add the new exercise
        self.add_exercise_button = ctk.CTkButton(self.box, text="Add Exercise", command=self.add_exercise, text_color="#0C0C0C", font=ctk.CTkFont(size=25), fg_color="#298031", hover_color="#1F6326", border_width=2, border_color="#000000", corner_radius=20, width=250)
        self.add_exercise_button.grid(row=2, column=0, padx=10, pady=(10, 10))


        # Button to go back to the main screen
        self.back_button = ctk.CTkButton(self, corner_radius=0, fg_color="#FF1E1E", hover_color="#CB1919", text="Exit to Home Screen", command=lambda: controller.show_frame(HomeScreen), font=ctk.CTkFont(size=15), border_color="#000000", border_width=2, text_color="#0C0C0C")
        self.back_button.grid(row=2, column=1, pady=(10, 10), padx=10, sticky='s')


    def add_exercise(self):
        """Adds a new exercise to the list."""
        new_exercise = self.new_exercise_entry.get()
        # Check if the new exercise is not empty and not already in the list
        if new_exercise not in self.manager.all_exercises:
            self.manager.add_exercise(new_exercise)
            # Clear the entry field
            self.new_exercise_entry.delete(0, 'end')
            self.manager.save_data()
            # print(f"Exercise '{new_exercise}' added.")


            for widget in self.exercise_scrollframe.winfo_children():
                widget.destroy()

            for exercise in self.manager.all_exercises:  # Load exercises from the manager
                label = ctk.CTkLabel(self.exercise_scrollframe, text=f"- {exercise}", anchor="w", font=ctk.CTkFont(size=25), text_color="#0C0C0C")
                label.grid(sticky="w", padx=10, pady=2)

        else:
            print("Exercise already exists or is empty.")
