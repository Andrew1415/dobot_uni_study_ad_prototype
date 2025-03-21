import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

import random
import logging

from .communication import request_prize, send_candy_robot_command, send_leaflet_robot_command, RESPONSE_SUCCESS, RESPONSE_TIMEOUT
from .question_bank import next_question, categories
from .camera_capture import find_candy
import threading

COUNTDOWN_STEP = 1500

candy1_img = Image.open("img/candy1.png")
CANDY1 = candy1_img

candy2_img = Image.open("img/candy2.png")
CANDY2 = candy2_img

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
def view_incorrect_answer(frame, redirect_func):
    clear_frame(frame)

    incorrect_label = tk.Label(frame, text="Atsakymas neteisingas. Bandykite dar kartą.", font=("Rando", 30))
    incorrect_label.pack(pady=20)

    frame.after(2000, lambda: redirect_func(frame))

def view_answer_question(frame, category):
    clear_frame(frame)

    question_data = next_question(category)

    question_label = tk.Label(frame, text=question_data["question"], font=("Rando", 20))
    question_label.pack(pady=20)

    answers = [question_data["correct_answer"]] + question_data["incorrect_answers"]
    random.shuffle(answers)

    def process_answer(answer):
        if answer == question_data["correct_answer"]:
            view_pick_candy(frame, category)
        else:
            view_incorrect_answer(frame, redirect_func=view_pick_quiz_category)

    for answer in answers:
        answer_button = tk.Button(frame, command=lambda answer=answer: process_answer(answer),
                                  text=answer, font=("Rando", 15), width=100, height=2, borderwidth=1, relief="solid")
        answer_button.pack(pady=5)

def view_take_candy(frame, candy, category):
    clear_frame(frame)

    text_label = tk.Label(frame, text="Pasiimkite saldainį ir kortelę 😄", font=("Rando", 25))
    text_label.pack(pady=20)

    countdown_label = tk.Label(frame, font=("Rando", 25), text="Atsargiai! Geri robotai, bet turi silpnus nervus.")
    countdown_label.pack()

    best_cell = find_candy(candy)
    place = f"{best_cell[0]},{best_cell[1]}" 

    # counting_task = None

    def after_given_prize(response):
        # nonlocal counting_task

        # # Cancel counting task
        # if counting_task is not None:
        #     frame.after_cancel(counting_task)
        #     counting_task = None

        view_pick_quiz_category(frame)

    # def countdown(count):
    #     nonlocal counting_task
    #     countdown_label['text'] = count

    #     if count > 1:
    #         counting_task = frame.after(COUNTDOWN_STEP, countdown, count-1)

    threading.Thread(target=request_prize, args=(place, category, after_given_prize), daemon=True).start()
    # countdown(3)

def view_pick_candy(frame, category):
    clear_frame(frame)

    answer_label = tk.Label(frame, text="Sveikiname! Atsakėte teisingai.", font=("Rando", 30))
    answer_label.pack(pady=20)

    question_label = tk.Label(frame, text="Kokio saldainio norite?", font=("Rando", 30))
    question_label.pack(pady=20)

    candy1_button = tk.Button(frame, command=lambda: view_take_candy(frame, CANDY1, category), 
                               width=250, height=250, image=candy1_img, borderwidth=0, relief="solid")
    candy1_button.pack(side=tk.LEFT, padx=10)

    candy2_button = tk.Button(frame, command=lambda: view_take_candy(frame, CANDY2, category), 
                               width=250, height=250, image=candy2_img, borderwidth=0, relief="solid")
    candy2_button.pack(side=tk.RIGHT, padx=10)

def view_pick_quiz_category(frame):
    clear_frame(frame)

    category_label = tk.Label(frame, text="Pasirinkite kategoriją", font=("Rando", 25))
    category_label.pack(pady=2)
    
    category_frame = tk.Frame(frame)
    category_frame.pack()

    row, col = 0, 0
    for category in categories.keys():
        category_button = tk.Button(category_frame, command=lambda category=category: view_answer_question(frame, category), 
                                    text=category, font=("Rando", 15), width=25, height=2, borderwidth=1, relief="solid")
        category_button.grid(row=row, column=col, padx=5, pady=5)
        
        col += 1
        if col > 1:  # Two columns
            col = 0
            row += 1

    #for category in categories.keys():
     #   category_button = tk.Button(frame, command=lambda category=category: view_answer_question(frame, category), 
     #                               text=category, font=("Rando", 25), width=15, height=2, borderwidth=0, relief="solid")
     #   category_button.pack(pady=10)

# Loads used images and set up their sizes
def load_logos():
    global ku_img, conexus_img, fondas_img, candy1_img, candy2_img

    # University logos
    ku_img = Image.open("img/ku.png")
    ku_img = ku_img.resize((188, 50))
    ku_img = ImageTk.PhotoImage(ku_img)

    conexus_img = Image.open("img/conexus.png")
    conexus_img = conexus_img.resize((120, 50))
    conexus_img = ImageTk.PhotoImage(conexus_img)

    fondas_img = Image.open("img/fondas.png")
    fondas_img = fondas_img.resize((140, 45))
    fondas_img = ImageTk.PhotoImage(fondas_img)

    # Candy logos
    candy1_img = candy1_img.resize((250, 250))
    candy1_img = ImageTk.PhotoImage(candy1_img)


    candy2_img = candy2_img.resize((250, 250))
    candy2_img = ImageTk.PhotoImage(candy2_img)

def setup_window():
    logging.info("Creating window...")

    # Setup window
    root = tk.Tk()
    root.title("Saldainiai")

    root.attributes('-fullscreen', True)

    # For raspberry
    root.attributes('-type', 'splash')

    # Load logos used in the application
    load_logos()

    # Setup header of the window
    frame_header = tk.Frame(root)
    frame_header.pack(expand=True)

    # Display logos in the header
    conexus_logo = tk.Label(frame_header, height=120, image=conexus_img, borderwidth=0, relief="solid")
    conexus_logo.grid(row = 0, column = 0, padx=1)

    ku_logo = tk.Label(frame_header, height=120, image=ku_img, borderwidth=0, relief="solid")
    ku_logo.grid(row = 0, column = 1, padx=1)

    fondas_logo = tk.Label(frame_header, height=120, image=fondas_img, borderwidth=0, relief="solid")
    fondas_logo.grid(row = 0, column = 2, padx=1)

    def on_exit():
        result = messagebox.askquestion("Exit", "Ar tikrai norite išeiti?")
        if result == "yes":
            logging.info('Destroying window...')
            root.destroy()

    # Display exit button
    exit_button = tk.Button(root, text="X", font=("Rando", 20), command=on_exit, fg="white", bg="red")
    exit_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    # Setup main content of window
    frame_content = tk.Frame(root)
    frame_content.pack(expand=True)

    # Display question frame first
    view_pick_quiz_category(frame_content)

    # Main loop
    root.mainloop()

