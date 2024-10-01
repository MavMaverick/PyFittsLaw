import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import PhotoImage  # Import the PhotoImage class from tkinter for images
from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow for image handling
# The pip package name and python/import package name do not have to be the same. Since pillow
# is meant to replace PIL, it uses the same import name for compatibility. PIL is Pillow
from tkinter import IntVar  # Import IntVar for storing integer values
import random
import time
import os
import uuid
import csv
import pygame

# True disables, fullscreen and value printing per trial
debugger = True
# debugger = False

# Initialize Pygame Mixer
pygame.mixer.init()
click_sound = pygame.mixer.Sound("hitmarker_2.mp3")

# Global variable for the image reference
global photo1
global photo2
global photo3

def on_agree():
    # Function for handling agreement to consent
    print("     Consent given. Starting experiment...")
    root.destroy()

def on_disagree(root):
    # Function for handling disagreement to consent
    root.destroy()
    exit()

def on_scroll(event, txt_consent, btn_agree):
    # Function to handle the scroll event
    if txt_consent.yview()[1] == 1.0:
        btn_agree.pack(side=tk.LEFT, padx=20)

def setup_consent_screen(root):
    global photo  # Declare photo as global to keep the reference

    consent_text = """Please read the following informed consent document. 

If you want to consent to the study, please continue reading until the end.
If you do not consent and would like to cancel your participation in the study, you can stop here.

Project Title: CS470 HCI - Fitts' Law study

Research Team:
 Karter Prehn(kd9566gs@go.minnstate.edu)

Thank you for agreeing to participate in this research study! This document provides important
information about what you will be asked to do during the research study, about the risks and benefits
of the study, and about your rights as a research subject. If you have any questions about or do not
understand something in this document, you should ask questions to the members of the research team
listed above. 

DO NOT AGREE to participate in this research study unless the research team has answered
your questions and you decide that you want to be part of this study.
The purpose of this research study is to evaluate how accurately a user can click on differently-sized
circles on screen. 

During the study, you will be randomly presented with blue circles of different sizes. There will be a total of 320 trials, and each trial will take anywhere from 3 to 5 seconds, depending on your speed. The entire
study should take no longer than 4 minutes to complete.

To participate in this study, you must be familiar with using a computer mouse and be at least 18 years of age.

To collect data, our software will record how much you move the mouse, how long it takes you to
successfully complete each trial, whether you make any errors, and if you are a HCI student. This information will be recorded
anonymously, and no personally identifiable information will be collected.

You will be compensated for your participation in this study with a drink or snack supplied at the end of the test. We do not believe there are any direct
benefits to you based on your participation in the study. We do not anticipate any significant risks in
your participating in this study.

You may end your participation in the study at any time. If you wish to end your participation, please
notify one of the researchers. If you decide to end your participation early, any results collected by the
software for your session will not be saved.

By clicking "Agree", you hereby acknowledge that you are at least 18 years of age, and that you areb familiar with using a computer mouse.

You also indicate that you agree to the following statement:
“I have read this consent form and I understand the risks, benefits, and procedures involved with
participation in this research study. I hereby agree to participate in this research study.”
"""  # Placeholder for your consent text

    txt_consent = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, font=("Helvetica", 14))  # Adjust font size as needed
    txt_consent.insert(tk.INSERT, consent_text)
    txt_consent.config(state=tk.DISABLED)  # Makes the text read-only
    txt_consent.pack(pady=10)
    txt_consent.bind("<MouseWheel>", lambda event: on_scroll(event, txt_consent, btn_agree))

    # Create a label for the HCI student question with a bigger font
    hci_label = tk.Label(root, text="Are you an HCI student?", font=("Helvetica", 16))
    hci_label.place(x=40, y=570)

    # Create a checkbox for HCI student status with a bigger size
    global HCI_var  # Declare HCI_var as a global variable
    HCI_var = tk.IntVar()
    hci_checkbox = tk.Checkbutton(root, text="checkmark if 'Yes'", variable=HCI_var, font=("Helvetica", 16))
    hci_checkbox.place(x=70, y=600)

    # Load and display the first image
    image_path1 = "scroll_down.png"
    image1 = Image.open(image_path1)
    image1 = image1.resize((190, 190))
    global photo1  # Declare photo1 as a global variable to retain it
    photo1 = ImageTk.PhotoImage(image1)
    img_label1 = tk.Label(root, image=photo1)
    img_label1.place(x=1089, y=150)

    # Load and display the second image
    image_path2 = "click_diagram.png"
    image2 = Image.open(image_path2)
    image2 = image2.resize((430, 160))
    global photo2  # Declare photo2 as a global variable to retain it
    photo2 = ImageTk.PhotoImage(image2)
    img_label2 = tk.Label(root, image=photo2)
    img_label2.place(x=400, y=470)

        # Load and display the third image
    image_path3 = "HCI.png"
    image3 = Image.open(image_path3)
    image3 = image3.resize((60, 60))
    global photo3  # Declare photo3 as a global variable to retain it
    photo3 = ImageTk.PhotoImage(image3)
    img_label3 = tk.Label(root, image=photo3)
    img_label3.place(x=280, y=570)



    # Creating the Agree and Disagree buttons with increased size and text size
    btn_agree = tk.Button(root, text="I Agree", command=on_agree, width=30, height=3, bg='green', fg='white', font=("Helvetica", 14))
    btn_disagree = tk.Button(root, text="I Disagree", command=lambda: on_disagree(root), bg='red', fg='white', width=30, height=3, font=("Helvetica", 14))
    btn_disagree.pack(side=tk.RIGHT, padx=20)

root = tk.Tk()
root.title("Fitts' Law Experiment: INFORMED CONSENT")
root.geometry("1280x900")  # width x height
root.overrideredirect(True)  # Remove window decorations
setup_consent_screen(root)

root.mainloop()



if HCI_var.get() == 1:
    subject_type = 1
    print("User is an HCI student")
else:
    subject_type = 0
    print("User is not an HCI student")


# pyautogui breaks th buttons on the consent window, for some reason
import pyautogui

# At the beginning or start of the experiment
participant_id = str(uuid.uuid4())

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
CIRCLE_SIZES = [40, 80, 120, 200]
CENTER_BOX_SIZE, MIDPOINT = 10, SCREEN_WIDTH // 2
HALF_MAX_CIRCLE_SIZE = max(CIRCLE_SIZES) // 2
OFFSET = SCREEN_WIDTH * 1 // 16
REPS_PER_CONFIGURATION = 10
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
    headers = ['Participant_UIDD','Target_size','Distance_from_center','Screen_side','Trial_time','Pixels_travelled','Click_errors','Subject_type']
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
            entry["Participant_UIDD"] = participant_id
            writer.writerow(entry)

# Function to handle circle click
def on_circle_click(event, canvas, circle_id, configurations, counter_id):
    global successful_clicks, total_cursor_movement, unsuccessful_clicks, trial_start_time, current_trial_configuration
    click_sound.play()
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
        "Participant_UIDD": participant_id,
        "Target_size": size,
        "Distance_from_center": x_distance,
        "Screen_side": direction,
        "Trial_time": round(elapsed_time, 2),  # Time rounded to 2 decimal places
        "Pixels_travelled": round(total_cursor_movement, 2),  # Distance rounded to 2 decimal places
        "Click_errors": unsuccessful_clicks - 1,
        "Subject_type": subject_type
    }

    trial_data_list.append(trial_data)

    if debugger == True:
        print(f"Trial data: Participant_UIDD: {participant_id}, Target_size: {size}, Distance_from_center: {x_distance}, Screen_side: {direction}, Trial_time: {elapsed_time:.2f} sec, Pixels_travelled: {total_cursor_movement:.2f} pixels, Click_errors: {unsuccessful_clicks - 1}, Subject_type: {subject_type}")

    # print(f"Time for this trial: {elapsed_time} seconds")
    canvas.delete(circle_id)  # Remove the clicked circle
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
            # Hide the click counter
            canvas.delete(counter_id)
            canvas.delete(center_box)
            
            # Calculate total time and errors
            total_time = sum([trial['Time'] for trial in trial_data_list])
            total_errors = sum([trial['Errors'] for trial in trial_data_list])
            
            # Display completion information
            completion_message = f"Thank you for participating!\nTotal Time: {total_time:.2f} seconds\nTotal Errors: {total_errors}"
            canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text=completion_message, fill="lightgreen", font=('Helvetica', 46), tags="completion_info")
            
            # Wait a bit before closing to allow user to read the message
            canvas.after(10000, lambda: root.destroy())  # Adjust the delay as needed

            print("\nExperiment completed, exporting data...")
            save_data_to_csv(trial_data_list)
            print("\033[92mCSV data succesfully appended.\033[0m")
            # root.destroy()  # This line is moved into the lambda function above
            # exit()  # Not required since root.destroy() will close the app

    
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

def printHi():
    print("hi")

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
    print("\n\033[91mEXITED, DATA NOT SAVED\033[0m")
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

center_box = canvas.create_rectangle((SCREEN_WIDTH / 2 - CENTER_BOX_SIZE / 2, SCREEN_HEIGHT / 2 - CENTER_BOX_SIZE / 2),
                        (SCREEN_WIDTH / 2 + CENTER_BOX_SIZE / 2, SCREEN_HEIGHT / 2 + CENTER_BOX_SIZE / 2),
                        fill='black')

# This will place the clicks counter below the center black box and change the color to white.
# Ensure this line is after the canvas is created and packed
counter_id = canvas.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + CENTER_BOX_SIZE + 40, text=f"0/{TOTAL_TRIALS} Clicks", fill="white", font=('Helvetica', '26'))

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


print("\nScreen Size: ", screen_width, "x", screen_height)
print("Midpoint: ", MIDPOINT)
configurations = generate_configurations()
random.shuffle(configurations)
root.mainloop()



