import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

COUNTDOWN_STEP = 1500
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

FORTUNA = "fortuna"
ANANASAS = "ananasas"

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

    # Remembers if robot has returned a signal, to prevent countdown
    robot_responded = False

    def on_robot_response():
        nonlocal robot_responded
        robot_responded = True

        view_select_candy()

    def show_count(count):
        nonlocal robot_responded
        if robot_responded:
            # If robot already responded, do not continue counting
            return

        countdown.config(text=str(count))

    frame_content.after(1 * COUNTDOWN_STEP, lambda: show_count(3))
    frame_content.after(2 * COUNTDOWN_STEP, lambda: show_count(2))
    frame_content.after(3 * COUNTDOWN_STEP, lambda: show_count(1))

    # Countdown to return to main page
    frame_content.after(4 * COUNTDOWN_STEP, on_robot_response)

def view_select_candy():
    clear_frame(frame_content)

    question_label = tk.Label(frame_content, text="Kokio saldainio norite?", font=("Rando", 30))
    question_label.pack(pady=20)

    fortune_button = tk.Button(frame_content, command=lambda: view_catch_candy(FORTUNA), width=300, height=200, image=fortuna_img, borderwidth=0, relief="solid")
    fortune_button.pack(side=tk.LEFT, padx=10)

    ananasu_button = tk.Button(frame_content, command=lambda: view_catch_candy(ANANASAS), width=300, height=200, image=ananasas_img, borderwidth=0, relief="solid")
    ananasu_button.pack(side=tk.RIGHT, padx=10)

# Loads used images and set up their sizes
def load_logos():
    global ku_img, conexus_img, fondas_img, fortuna_img, ananasas_img

    # University logos
    ku_img = Image.open("src/img/ku.png")
    ku_img = ku_img.resize((150, 87))
    ku_img = ImageTk.PhotoImage(ku_img)

    conexus_img = Image.open("src/img/conexus.png")
    conexus_img = conexus_img.resize((200, 100))
    conexus_img = ImageTk.PhotoImage(conexus_img)

    fondas_img = Image.open("src/img/fondas.png")
    fondas_img = fondas_img.resize((100, 35))
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
    conexus_logo = tk.Label(frame_header, width=300, height=100, image=conexus_img, borderwidth=0, relief="solid")
    conexus_logo.pack(side=tk.LEFT, padx=10)

    ku_logo = tk.Label(frame_header, width=300, height=60, image=ku_img, borderwidth=0, relief="solid")
    ku_logo.pack(side=tk.LEFT, padx=10)

    fondas_logo = tk.Label(frame_header, width=200, height=100, image=fondas_img, borderwidth=0, relief="solid")
    fondas_logo.pack(side=tk.LEFT, padx=10)

    # Display close button
    exit_button = tk.Button(window, text="X", font=("Rando", 20), command=on_exit)
    exit_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    # Setup main content of window
    global frame_content
    frame_content = tk.Frame(window)
    frame_content.pack(expand=True)

    # Display main interface
    view_select_candy()

    # Window loop
    window.mainloop()

def main():
    try:
        setup_window()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
