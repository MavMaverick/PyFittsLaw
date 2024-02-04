import tkinter as tk
from tkinter import ttk
import random
import pyautogui
import time
import os
import uuid
import csv
import consent_screen  # Import the consent screen module

# At the beginning or start of the experiment
participant_id = str(uuid.uuid4())


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
CIRCLE_SIZES = [40, 50, 60, 70]
CENTER_BOX_SIZE, MIDPOINT = 10, SCREEN_WIDTH // 2
HALF_MAX_CIRCLE_SIZE = max(CIRCLE_SIZES) // 2
OFFSET = SCREEN_WIDTH * 1 // 16
REPS_PER_CONFIGURATION = 1
TOTAL_TRIALS = 32 * REPS_PER_CONFIGURATION

# Global Variables
successful_clicks, unsuccessful_clicks, trial_start_time = 0, 0, 0
last_cursor_position, total_cursor_movement = None, 0
trial_data_list = []

# Function to start the experiment
def start_experiment(event):
    global start_button, start_text, configurations, counter_id
    remove_existing_circle(canvas)
    canvas.delete(start_button)  # Remove the start button
    canvas.delete(start_text)    # Remove the start text
    start_trial(canvas, configurations, counter_id)  # Start the first trial
    reset_cursor_to_center(canvas)  # Reset cursor to center


# Function to update the visual counter and progress bar
def update_click_counter(canvas, counter_id):
    global successful_clicks
    canvas.itemconfig(counter_id, text=f"{successful_clicks}/{TOTAL_TRIALS} Clicks")
    progress_var.set(successful_clicks)  # Update the progress bar

# Function to show success message
def show_success_message(canvas):
    # Create the text message
    success_text = canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + -50, text="GOOD! 1+", fill="light green", font=('Helvetica', '30'))
    # Schedule the message to be removed after 500ms
    canvas.after(500, lambda: canvas.delete(success_text))

# Function to save trial data to CSV
def save_data_to_csv(data, filepath='experiment_data.csv'):
    # Define the CSV file headers
    headers = ["Participant_ID", "Size", "Position", "Direction", "Time", "Distance", "Errors"]
    # Check if the file already exists
    file_exists = os.path.isfile(filepath)
    # Open file in append mode
    with open(filepath, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # Write header only if the file is new
        if not file_exists:
            writer.writeheader()
        for entry in data:
            # Add participant ID to each entry
            entry["Participant_ID"] = participant_id
            writer.writerow(entry)

# Function to handle circle click
def on_circle_click(event, canvas, circle_id, configurations, counter_id):
    global successful_clicks, total_cursor_movement, unsuccessful_clicks, trial_start_time, current_trial_configuration
    elapsed_time = time.time() - trial_start_time
    size, x_pos = current_trial_configuration
    #   MIDPOINT is used to negate and find the distance from center of the x_pos
    if x_pos < MIDPOINT:
        direction = "left"
        x_distance = MIDPOINT - x_pos
    else:
        direction = "right"
        x_distance = x_pos - MIDPOINT


        # Storing trial data
    trial_data = {
        "Size": size,
        "Position": x_distance,
        "Direction": direction,
        "Time": round(elapsed_time, 2),  # Time rounded to 3 decimal places
        "Distance": round(total_cursor_movement, 2),  # Distance rounded to 2 decimal places
        "Errors": unsuccessful_clicks - 1
    }
    trial_data_list.append(trial_data)

    print(f"Trial data: Size: {size}, Position: {x_pos}, Direction: {direction}, Time: {elapsed_time:.2f} sec, Distance: {total_cursor_movement:.2f} pixels, Errors: {unsuccessful_clicks - 1}")
    # print(f"Time for this trial: {elapsed_time} seconds")
    canvas.delete(circle_id)
    successful_clicks += 1
    update_click_counter(canvas, counter_id)
    show_success_message(canvas)
    # print(f"Total cursor movement for this trial: {total_cursor_movement} pixels")
    # print(f"Unsuccessful clicks for this trial: {unsuccessful_clicks - 1}")
    unsuccessful_clicks = 0
    reset_cursor_to_center(canvas)
    if configurations:  # Check if there are still configurations left
        start_trial(canvas, configurations, counter_id)  # Start the next trial
    else:
        # Place this inside the on_circle_click function, after incrementing successful_clicks
        if successful_clicks == TOTAL_TRIALS:
            print(f"All configurations were presented {REPS_PER_CONFIGURATION} time(s) each.")
            # Remove the exit button and text once the experiment is completed
            canvas.delete(exit_rectangle)
            canvas.delete(exit_text)
            print("\nExperiment completed, exporting data...")
            save_data_to_csv(trial_data_list)
            print("CSV data appended.")

    
def on_any_click(event):
    global unsuccessful_clicks
    unsuccessful_clicks += 1

def on_mouse_move(event):
    global last_cursor_position, total_cursor_movement
    current_position = (event.x, event.y)
    
    if last_cursor_position is not None:
        movement = ((current_position[0] - last_cursor_position[0])**2 + 
                    (current_position[1] - last_cursor_position[1])**2) ** 0.5
        total_cursor_movement += movement

    last_cursor_position = current_position

# Function to start a trial
def start_trial(canvas, configurations, counter_id):
    global trial_start_time, total_cursor_movement, last_cursor_position, current_trial_configuration
    total_cursor_movement = 0
    last_cursor_position = None

    if not configurations:  # Check if configurations list is empty
        print("Experiment completed")
        return  # Exit if all trials are completed

    current_trial_configuration = configurations.pop()  # Store and remove the current trial configuration
    trial_start_time = time.time()  # Record the start time

    size, x_pos = current_trial_configuration
    y_pos = SCREEN_HEIGHT / 2

    # Create the circle
    circle_id = canvas.create_oval(x_pos - size / 2, y_pos - size / 2,
                                   x_pos + size / 2, y_pos + size / 2, fill='blue')

    # Bind the click event
    canvas.tag_bind(circle_id, '<Button-1>', lambda event: on_circle_click(event, canvas, circle_id, configurations, counter_id))


# Function to reset the cursor to the center of the screen
def reset_cursor_to_center(canvas):
    center_x = canvas.winfo_rootx() + canvas.winfo_width() / 2
    center_y = canvas.winfo_rooty() + 20 + canvas.winfo_height() / 2
    pyautogui.moveTo(center_x, center_y)

# Function to exit the program
def exit_program(event):
    print('\nEXIT, ALL DATA HAS NOT BEEN SAVED')
    root.destroy()


# Generate all possible configurations
def generate_configurations():
    configurations = []
    for size in CIRCLE_SIZES:
        for position in X_POSITIONS['left'] + X_POSITIONS['right']:
            configurations.append((size, position))
    
    # Replicate each configuration based on the number of repetitions
    configurations *= REPS_PER_CONFIGURATION
    
    if len(configurations) != TOTAL_TRIALS:
        raise ValueError(f"Unexpected number of configurations. Expected {TOTAL_TRIALS}, got {len(configurations)}")
    
    return configurations

# Update TOTAL_TRIALS
TOTAL_TRIALS = 32 * REPS_PER_CONFIGURATION


def remove_existing_circle(canvas, circle_tag='current_circle'):
    existing_circle = canvas.find_withtag(circle_tag)
    if existing_circle:
        canvas.delete(existing_circle)


# Simplified and adjusted positions
X_POSITIONS = {
    'left': [
        MIDPOINT - OFFSET - (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE),
        MIDPOINT - OFFSET * 2 - (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE),
        MIDPOINT - OFFSET * 3 - (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE),
        MIDPOINT - OFFSET * 4 - (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE)
    ],
    'right': [
        MIDPOINT + OFFSET + (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE),
        MIDPOINT + OFFSET * 2 + (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE),
        MIDPOINT + OFFSET * 3 + (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE),
        MIDPOINT + OFFSET * 4 + (CENTER_BOX_SIZE // 2 + HALF_MAX_CIRCLE_SIZE)
    ]
}

# Ensure positions do not exceed screen bounds
X_POSITIONS['left'] = [max(pos, HALF_MAX_CIRCLE_SIZE) for pos in X_POSITIONS['left']]
X_POSITIONS['right'] = [min(pos, SCREEN_WIDTH - HALF_MAX_CIRCLE_SIZE) for pos in X_POSITIONS['right']]


# Set up the main application window
root = tk.Tk()

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Remove window decorations
root.overrideredirect(True)

root.title("Fitts' Law Experiment")
root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
# Set the background color of the application window
root.configure(bg='gray')  # For gray background

# Add the progress bar to the main application window (before creating and packing the canvas)
progress_var = tk.DoubleVar()  # The variable that holds the progress value.
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=TOTAL_TRIALS, length=SCREEN_WIDTH - 20)
progress_bar.pack(side="bottom", fill="x", padx=10, pady=10)

# Now create and pack the canvas
canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='gray')
canvas.pack(expand=tk.YES, fill=tk.BOTH)

canvas.create_rectangle((SCREEN_WIDTH / 2 - CENTER_BOX_SIZE / 2, SCREEN_HEIGHT / 2 - CENTER_BOX_SIZE / 2),
                        (SCREEN_WIDTH / 2 + CENTER_BOX_SIZE / 2, SCREEN_HEIGHT / 2 + CENTER_BOX_SIZE / 2),
                        fill='black')

# This will place the clicks counter below the center black box and change the color to white.
# Ensure this line is after the canvas is created and packed
counter_id = canvas.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + CENTER_BOX_SIZE + 40, text=f"0/{TOTAL_TRIALS} Clicks", fill="white", font=('Helvetica', '16'))

# Define the size of the exit button
exit_button_width = 100
exit_button_height = 50

# Create a rectangle at the bottom of the canvas that serves as an "Exit" button
exit_button_x = SCREEN_WIDTH / 2
exit_button_y = SCREEN_HEIGHT - exit_button_height * 2
exit_rectangle = canvas.create_rectangle(exit_button_x - exit_button_width / 2, exit_button_y - exit_button_height / 2,
                                         exit_button_x + exit_button_width / 2, exit_button_y + exit_button_height / 2,
                                         fill='red')

# Add "Exit" text over the rectangle
exit_text = canvas.create_text(exit_button_x, exit_button_y, text="EXIT?", fill="white", font=('Helvetica', '16'))

# Instead of starting the first trial immediately, create a start button
start_button = canvas.create_rectangle((SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 25),
                                       (SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT / 2 + 25),
                                       fill='green')
start_text = canvas.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text="START?", fill="white", font=('Helvetica', '20'))


# Bindings and Initializations
    # update binding for mouse movement in tkinter
canvas.bind("<Motion>", on_mouse_move)
    # update binding for usuccesful clciks 
canvas.bind("<Button-1>", on_any_click)
    # Bind the click event on the start button to start the experiment
canvas.tag_bind(start_button, '<Button-1>', start_experiment)
canvas.tag_bind(start_text, '<Button-1>', start_experiment)
    # Update the bindings for the new exit button
canvas.tag_bind(exit_rectangle, '<Button-1>', exit_program)
canvas.tag_bind(exit_text, '<Button-1>', exit_program)

    # Start the Application
print("\nScreen Size: ", screen_width, "x", screen_height)
print("Midpoint: ", MIDPOINT)
configurations = generate_configurations()
random.shuffle(configurations)

# Create the Tkinter root window
root = tk.Tk()
root.geometry("1920x1200")  # Adjust size as needed for your consent screen

# Initialize the consent screen with the root window
consent_screen.setup_consent_screen(root)  # Pass the root window as an argument

# The consent screen should handle closing itself and starting the experiment,
# so you may need a mechanism to wait for consent before continuing
root.mainloop()  # This will display the window and wait for interaction
root.mainloop()

