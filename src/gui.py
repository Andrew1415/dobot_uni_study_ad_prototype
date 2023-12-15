import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from candy import FORTUNA, ANANASAS, request_candy, setup_communication, close_communication
from question_bank import next_question, categories
import random

COUNTDOWN_STEP = 1500
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

def on_exit():
    result = messagebox.askquestion("Exit", "Ar tikrai norite išeiti?")
    if result == "yes":
        window.destroy()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def view_catch_candy(candy):
    clear_frame(frame_content)

    label = tk.Label(frame_content, text="Gaudykite saldainį!", font=("Rando", 25))
    label.pack(pady=20)

    countdown = tk.Label(frame_content, font=("Rando", 25))
    countdown.pack()

    # Remembers if the robot has returned a signal, to prevent countdown
    robot_responded = False

    def on_robot_response():
        nonlocal robot_responded
        robot_responded = True

        view_select_category()

    def show_count(count):
        nonlocal robot_responded
        if robot_responded:
            # If the robot already responded, do not continue counting
            return

        countdown.config(text=str(count))

    request_candy(candy, on_robot_response)

    frame_content.after(1 * COUNTDOWN_STEP, lambda: show_count(3))
    frame_content.after(2 * COUNTDOWN_STEP, lambda: show_count(2))
    frame_content.after(3 * COUNTDOWN_STEP, lambda: show_count(1))
    
def view_select_candy():
    clear_frame(frame_content)

    question_label = tk.Label(frame_content, text="Sveikiname! Atsakėte teisingai.", font=("Rando", 30))
    question_label.pack(pady=20)
    question_label = tk.Label(frame_content, text="Kokio saldainio norite?", font=("Rando", 30))
    question_label.pack(pady=20)

    # Display answer buttons
    fortune_button = tk.Button(frame_content, command=lambda: view_catch_candy(FORTUNA), width=300, height=200, image=fortuna_img, borderwidth=0, relief="solid")
    fortune_button.pack(side=tk.LEFT, padx=10)

    ananasu_button = tk.Button(frame_content, command=lambda: view_catch_candy(ANANASAS), width=300, height=200, image=ananasas_img, borderwidth=0, relief="solid")
    ananasu_button.pack(side=tk.RIGHT, padx=10)

def view_select_category():
    clear_frame(frame_content)

    category_label = tk.Label(frame_content, text="Pasirinkite kategoriją", font=("Rando", 35))
    category_label.pack(pady=20)

    # Display category buttons
    for category in categories.keys():
        category_button = tk.Button(frame_content, command=lambda cat=category: view_quiz(cat), text=category, font=("Rando", 25), width=15, height=2, borderwidth=0, relief="solid")
        category_button.pack(pady=10)

def view_quiz(current_category):
    clear_frame(frame_content)

    question_data = next_question(current_category)

    question_label = tk.Label(frame_content, text=question_data["question"], font=("Rando", 35))
    question_label.pack(pady=20)

    # Create a list with the correct and incorrect answers
    answers = [question_data["correct_answer"]] + question_data["incorrect_answers"]

    # Shuffle the answers to randomize their placement
    random.shuffle(answers)

    button_width = 15
    button_height = 2  # Set the desired height

    # Display answer buttons without labels
    for answer in answers:
        answer_button = tk.Button(frame_content, command=lambda ans=answer: check_answer(ans, question_data["correct_answer"]),
                                  text=answer, font=("Rando", 25), width=button_width, height=button_height, borderwidth=0, relief="solid")
        answer_button.pack(pady=5)

def show_incorrect_answer():
    clear_frame(frame_content)

    incorrect_label = tk.Label(frame_content, text="Atsakymas neteisingas. Bandykite dar kartą.", font=("Rando", 30))
    incorrect_label.pack(pady=20)

    # After two seconds, refresh and return to the quiz
    frame_content.after(2000, view_select_category)

def check_answer(answer, correct_answer):
    # Check if the answer is correct
    if answer == correct_answer:
        view_select_candy()  # Show the main content
    else:
        show_incorrect_answer()

# Loads used images and set up their sizes
def load_logos():
    global ku_img, conexus_img, fondas_img, fortuna_img, ananasas_img

    # University logos
    ku_img = Image.open("src/img/ku.png")
    ku_img = ku_img.resize((150, 170))
    ku_img = ImageTk.PhotoImage(ku_img)

    conexus_img = Image.open("src/img/conexus.png")
    conexus_img = conexus_img.resize((100, 50))
    conexus_img = ImageTk.PhotoImage(conexus_img)

    fondas_img = Image.open("src/img/fondas.png")
    fondas_img = fondas_img.resize((50, 17))
    fondas_img = ImageTk.PhotoImage(fondas_img)

    # Candy logos
    fortuna_img = Image.open("src/img/fortuna.png")
    fortuna_img = fortuna_img.resize((250, 200))
    fortuna_img = ImageTk.PhotoImage(fortuna_img)

    ananasas_img = Image.open("src/img/ananasas.png")
    ananasas_img = ananasas_img.resize((250, 250))
    ananasas_img = ImageTk.PhotoImage(ananasas_img)

def setup_window():
    # Create main window in fullscreen
    global window
    window = tk.Tk()
    window.title("Saldainiai")

    window.attributes('-fullscreen', True)
    window.attributes("-type", "splash")

    # Setup screen resolution (TODO: Is this part required?)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - WINDOW_WIDTH) // 2
    y_position = (screen_height - WINDOW_HEIGHT) // 2

    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_position}+{y_position}")

    # Load logos used in the application
    load_logos()

    # Setup header of the window
    global frame_header
    frame_header = tk.Frame(window)
    frame_header.pack(expand=True)

    # Display logos in the header
    conexus_logo = tk.Label(frame_header, width=300, height=100, justify="left", image=conexus_img, borderwidth=0, relief="solid")
    conexus_logo.pack(side=tk.LEFT, padx=1)

    ku_logo = tk.Label(frame_header, width=600, height=120, justify="center", image=ku_img, borderwidth=0, relief="solid")
    ku_logo.pack(side=tk.LEFT, padx=1)

    fondas_logo = tk.Label(frame_header, width=200, height=100, justify="right", image=fondas_img, borderwidth=0, relief="solid")
    fondas_logo.pack(side=tk.LEFT, padx=1)

    # Display close button
    exit_button = tk.Button(window, text="X", font=("Rando", 20), command=on_exit)
    exit_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    # Setup main content of window
    global frame_content
    frame_content = tk.Frame(window)
    frame_content.pack(expand=True)

    # Display question frame first
    view_select_category()

    # Window loop
    window.mainloop()

def main():
    try:
        setup_communication()
        setup_window()
    except Exception as e:
        print(e)
    finally:
        close_communication()

if __name__ == "__main__":
    main()