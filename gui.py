import tkinter as tk
import time
from tkinter import messagebox 
from PIL import Image, ImageTk

FORTUNA = "fortuna"
ANANASAS = "ananasas"

def on_exit():
    result = messagebox.askquestion("Exit", "Are you sure you want to exit?")
    if result == "yes":
        root.destroy()

root = tk.Tk()
root.title("Saldainiai")

root.attributes('-fullscreen', True)
root.attributes("-type", "splash")
# root.configure(bg="dark gray")

fortuna_img = Image.open("fortuna.png")
# fortuna_img = fortuna_img.resize((250, 250))
fortuna_img = ImageTk.PhotoImage(fortuna_img)

ananasas_img = Image.open("ananasas.png")
ananasas_img = ananasas_img.resize((150, 150))
ananasas_img = ImageTk.PhotoImage(ananasas_img)

ku_img = Image.open("ku.png")
ku_img = ku_img.resize((200, 125))
ku_img = ImageTk.PhotoImage(ku_img)

conexus_img = Image.open("conexus.png")
conexus_img = conexus_img.resize((200, 125))
conexus_img = ImageTk.PhotoImage(conexus_img)

fondas_img = Image.open("fondas.png")
fondas_img = fondas_img.resize((100, 50))
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

def pick_candy(candy):
    clear_frame()

    label = tk.Label(frame, text="Saldainis imamas...", font=("Helvetica", 25))
    label.pack()

    frame.after(3000, lambda: catch_candy(candy))

    # time.sleep(3)

    # return catch_candy(candy)


def catch_candy(candy):
    clear_frame()

    label = tk.Label(frame, text="Gaudykite saldainį!", font=("Helvetica", 25))
    label.pack(pady=20)

    countdown = tk.Label(frame, text=3, font=("Helvetica", 25))

    def show_count(count):
        countdown.config(text=count)

    frame.after(2000, lambda: countdown.pack())
    frame.after(4000, lambda: show_count(2))
    frame.after(6000, lambda: show_count(1))
    frame.after(10000, show_main_interface)


# Create the main window
def show_main_interface():
    clear_frame()

    question_label = tk.Label(frame, text="Kokio saldainio norite?", font=("Helvetica", 40))
    question_label.pack(pady=20)

    fortune_button = tk.Button(frame, command=lambda: pick_candy(FORTUNA), width=300, height=200, image=fortuna_img, borderwidth=0, relief="solid")
    fortune_button.pack(side=tk.LEFT, padx=10)

    ananasu_button = tk.Button(frame, command=lambda: pick_candy(ANANASAS), width=300, height=200, image=ananasas_img, borderwidth=0, relief="solid")
    ananasu_button.pack(side=tk.RIGHT, padx=10)
    
    exit_button = tk.Button(frame, text="X", font=("Helvetica", 20), command=on_exit)
    exit_button.place(x=window_width-40, y=10)

show_main_interface()
root.mainloop()