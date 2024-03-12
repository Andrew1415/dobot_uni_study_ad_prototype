import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
#from communication import FORTUNA, ANANASAS, request_candy, setup_communication, close_communication
from question_bank import next_question, categories
import random

FORTUNA = "fortuna"
ANANASAS = "ananasas"

COUNTDOWN_STEP = 1500
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

# View wrapper that clears the frame beforehand
def view(func):
    def wrapper(frame, *args, **kwargs):
        for widget in frame.winfo_children():
            widget.destroy()

        func(frame, *args, **kwargs)
    return wrapper

@view
def view_incorrect_answer(frame, redirect_view):
    incorrect_label = tk.Label(frame, text="Atsakymas neteisingas. Bandykite dar kartą.", font=("Rando", 30))
    incorrect_label.pack(pady=20)

    # After two seconds, refresh and return to the quiz
    frame.after(2000, lambda: redirect_view(frame))

@view
def view_answer_question(frame, category):
    def process_answer(answer, correct_answer):
        if answer == correct_answer:
            view_pick_candy(frame)
        else:
            view_incorrect_answer(redirect_view=view_pick_quiz_category)

    question_data = next_question(category)

    question_label = tk.Label(frame, text=question_data["question"], font=("Rando", 20))
    question_label.pack(pady=20)

    answers = [question_data["correct_answer"]] + question_data["incorrect_answers"]

    random.shuffle(answers)

    for answer in answers:
        answer_button = tk.Button(frame, command=lambda ans=answer: process_answer(ans, question_data["correct_answer"]),
                                  text=answer, font=("Rando", 25), width=2, height=100, borderwidth=0, relief="solid")
        answer_button.pack(pady=5)

@view
def view_pick_candy(frame, candy):
    label = tk.Label(frame, text="Gaudykite saldainį!", font=("Rando", 25))
    label.pack(pady=20)

    countdown = tk.Label(frame, font=("Rando", 25))
    countdown.pack()

    # Remembers if the robot has returned a signal, to prevent countdown
    robot_responded = False

    def on_robot_response():
        nonlocal robot_responded
        robot_responded = True

        view_pick_quiz_category(frame)

    def show_count(count):
        nonlocal robot_responded
        if robot_responded:
            # If the robot already responded, do not continue counting
            return

        countdown.config(text=str(count))

    #request_candy(candy, on_robot_response)

    frame.after(1 * COUNTDOWN_STEP, lambda: show_count(3))
    frame.after(2 * COUNTDOWN_STEP, lambda: show_count(2))
    frame.after(3 * COUNTDOWN_STEP, lambda: show_count(1))

@view
def view_pick_candy(frame):
    question_label = tk.Label(frame, text="Sveikiname! Atsakėte teisingai.", font=("Rando", 30))
    question_label.pack(pady=20)
    question_label = tk.Label(frame, text="Kokio saldainio norite?", font=("Rando", 30))
    question_label.pack(pady=20)

    # Display answer buttons
    fortune_button = tk.Button(frame, command=lambda: view_pick_candy(frame, FORTUNA), width=250, height=250, image=fortuna_img, borderwidth=0, relief="solid")
    fortune_button.pack(side=tk.LEFT, padx=10)

    ananasu_button = tk.Button(frame, command=lambda: view_pick_candy(frame, ANANASAS), width=250, height=250, image=ananasas_img, borderwidth=0, relief="solid")
    ananasu_button.pack(side=tk.RIGHT, padx=10)

@view
def view_pick_quiz_category(frame):
    category_label = tk.Label(frame, text="Pasirinkite kategoriją", font=("Rando", 35))
    category_label.pack(pady=20)

    # Display category buttons
    for category in categories.keys():
        category_button = tk.Button(frame, command=lambda: view_answer_question(frame, category), text=category, font=("Rando", 25), width=15, height=2, borderwidth=0, relief="solid")
        category_button.pack(pady=10)

# Loads used images and set up their sizes
def load_logos():
    global ku_img, conexus_img, fondas_img, fortuna_img, ananasas_img

    # University logos
    ku_img = Image.open("src/img/ku.png")
    ku_img = ku_img.resize((250, 80))
    ku_img = ImageTk.PhotoImage(ku_img)

    conexus_img = Image.open("src/img/conexus.png")
    conexus_img = conexus_img.resize((120, 50))
    conexus_img = ImageTk.PhotoImage(conexus_img)

    fondas_img = Image.open("src/img/fondas.png")
    fondas_img = fondas_img.resize((140, 45))
    fondas_img = ImageTk.PhotoImage(fondas_img)

    # Candy logos
    fortuna_img = Image.open("src/img/fortuna.png")
    fortuna_img = fortuna_img.resize((250, 250))
    fortuna_img = ImageTk.PhotoImage(fortuna_img)

    ananasas_img = Image.open("src/img/ananasas.png")
    ananasas_img = ananasas_img.resize((250, 250))
    ananasas_img = ImageTk.PhotoImage(ananasas_img)

def setup_window():
    root = tk.Tk()
    root.title("Saldainiai")

    root.attributes('-fullscreen', True)
    #root.attributes("-type", "splash")

    # Setup screen resolution (TODO: Is this part required?)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width - WINDOW_WIDTH) // 2
    y_position = (screen_height - WINDOW_HEIGHT) // 2

    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_position}+{y_position}")

    # Load logos used in the application
    load_logos()

    # Setup header of the window
    global frame_header
    frame_header = tk.Frame(root)
    frame_header.pack(expand=True)

    # Display logos in the header
    conexus_logo = tk.Label(frame_header, height=120, image=conexus_img, borderwidth=0, relief="solid")
    conexus_logo.grid(row = 0, column = 0, padx=10)

    ku_logo = tk.Label(frame_header, height=120, image=ku_img, borderwidth=0, relief="solid")
    ku_logo.grid(row = 0, column = 1, padx=10)

    fondas_logo = tk.Label(frame_header, height=120, image=fondas_img, borderwidth=0, relief="solid")
    fondas_logo.grid(row = 0, column = 2, padx=10)

    def on_exit():
        result = messagebox.askquestion("Exit", "Ar tikrai norite išeiti?")
        if result == "yes":
            root.destroy()

    # Display close button
    exit_button = tk.Button(root, text="X", font=("Rando", 20), command=on_exit)
    exit_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    # Setup main content of window
    global frame_content
    frame_content = tk.Frame(root)
    frame_content.pack(expand=True)

    # Display question frame first
    view_pick_quiz_category(frame_content)

    # Main loop
    root.mainloop()

def main():
    try:
        #setup_communication()
        setup_window()
    except Exception as e:
        raise
    finally:
        pass
        #close_communication()

if __name__ == "__main__":
    main()
