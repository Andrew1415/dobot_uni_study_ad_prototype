import tkinter as tk
import time
from tkinter import messagebox 
from PIL import Image, ImageTk
from candy import ANANASAS, FORTUNA, request_candy

def on_exit():
    result = messagebox.askquestion("Exit", "Ar tikrai norite išeiti?")
    if result == "yes":
        root.destroy()

root = tk.Tk()
root.title("Saldainiai")

root.attributes('-fullscreen', True)
root.attributes("-type", "splash")

fortuna_img = Image.open("src/img/fortuna.png")
fortuna_img = fortuna_img.resize((250, 200))
fortuna_img = ImageTk.PhotoImage(fortuna_img)

ananasas_img = Image.open("src/img/ananasas.png")
ananasas_img = ananasas_img.resize((250, 250))
ananasas_img = ImageTk.PhotoImage(ananasas_img)

ku_img = Image.open("src/img/ku.png")
ku_img = ku_img.resize((150, 87))
ku_img = ImageTk.PhotoImage(ku_img)

conexus_img = Image.open("src/img/conexus.png")
conexus_img = conexus_img.resize((200, 100))
conexus_img = ImageTk.PhotoImage(conexus_img)

fondas_img = Image.open("src/img/fondas.png")
fondas_img = fondas_img.resize((100, 35))
fondas_img = ImageTk.PhotoImage(fondas_img)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 1024
window_height = 600
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

logos = tk.Frame(root)
logos.pack(expand=True)

conexus_logo = tk.Label(logos, width=300, height=100, image=conexus_img, borderwidth=0, relief="solid")
conexus_logo.pack(side=tk.LEFT, padx=10)

ku_logo = tk.Label(logos, width=300, height=60, image=ku_img, borderwidth=0, relief="solid")
ku_logo.pack(side=tk.LEFT, padx=10)

fondas_logo = tk.Label(logos, width=200, height=100, image=fondas_img, borderwidth=0, relief="solid")
fondas_logo.pack(side=tk.LEFT, padx=10)

frame = tk.Frame(root)
frame.pack(expand=True)

def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()

#def pick_candy(candy):
#    clear_frame()
#
#    label = tk.Label(frame, text="Saldainis imamas...", font=("Rando", 25))
#    label.pack()
    
#    request_candy(candy, lambda: catch_candy(candy))
      
def pick_candy(candy):
    clear_frame()

    label = tk.Label(frame, text="Gaudykite saldainį!", font=("Rando", 25))
    label.pack(pady=20)

    countdown = tk.Label(frame, text=3, font=("Rando", 25))
    countdown.pack()
    received_signal = False

    def return_home():
        nonlocal received_signal
        print("Setting signal...")
        received_signal = True
        show_main_interface()

    def show_count(count):
        nonlocal received_signal
        print(f"Received signal {received_signal}")
        if received_signal:
            return

        countdown.config(text=str(count))

    request_candy(candy, return_home)

    frame.after(1000, lambda: show_count(3))
    frame.after(2000, lambda: show_count(2))
    frame.after(3000, lambda: show_count(1))

# Create the main window
def show_main_interface():
    clear_frame()

    question_label = tk.Label(frame, text="Kokio saldainio norite?", font=("Rando", 30))
    question_label.pack(pady=20)

    fortune_button = tk.Button(frame, command=lambda: pick_candy(FORTUNA), width=300, height=200, image=fortuna_img, borderwidth=0, relief="solid")
    fortune_button.pack(side=tk.LEFT, padx=10)

    ananasu_button = tk.Button(frame, command=lambda: pick_candy(ANANASAS), width=300, height=200, image=ananasas_img, borderwidth=0, relief="solid")
    ananasu_button.pack(side=tk.RIGHT, padx=10)
    
    exit_button = tk.Button(root, text="X", font=("Rando", 20), command=on_exit)
    exit_button.place(relx=1.0, x=-10, y=10, anchor="ne")

show_main_interface()
root.mainloop()