# Imports
import tkinter as tk
import pyautogui
import time
import threading
import os
import sys

# Global variable to manage typing
running = False

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and PyInstaller .exe """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Functions
def type():
    def countdown():
        for i in range(5, 0, -1):
            if not running:
                status_label.config(text="Stopped")
                return
            status_label.config(text=f"Starting in {i}...")
            window.update()
            time.sleep(1)
        status_label.config(text="Running...")
        window.update()

    def perform_typing():
        wpm = slider_value.get()
        text = entry.get("1.0", "end-1c")
        for char in text:
            if not running:
                status_label.config(text="Stopped")
                return
            pyautogui.typewrite(char, interval=3/(wpm*10))
        status_label.config(text="Completed!")

    global running
    running = True
    threading.Thread(target=lambda: [countdown(), perform_typing()]).start()

def stop_typing():
    global running
    running = False

def clear_entry():
    entry.delete("1.0", "end")

def move_slider(event):
    x = max(20, min(event.x, 280))  # Restrict movement within the slider range
    canvas.coords(knob, x - 10, 10, x + 10, 30)  # Move the slider knob
    slider_value.set(int((x - 20) / 260 * 9) + 1)  # Update the slider value (1-10)

# Window Setup
window = tk.Tk()
window.resizable(False, False)
window.title("Text to Type")
window.geometry("550x700")
window.configure(bg="#1e1e1e")  # Dark mode background

# Set Window and Taskbar Icon
icon_path = resource_path("icon.ico")
pngicon_path = resource_path("pngicon.png")

try:
    # Use .ico file for taskbar and window icon
    window.iconbitmap(icon_path)
except Exception as e:
    print(f"Could not load .ico file: {e}")

# Use .png file as a Tkinter PhotoImage for compatibility
try:
    png_icon = tk.PhotoImage(file=pngicon_path)
    window.tk.call('wm', 'iconphoto', window._w, png_icon)
except Exception as e:
    print(f"Could not load .png file: {e}")

# Elements
title = tk.Label(
    text="Text To Type",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="lightgray"
)
entry = tk.Text(
    window,
    width=50,
    height=10,
    bg="#2e2e2e",
    fg="lightgray",
    font=("Arial", 12),
    insertbackground="white",  # Cursor color
    highlightthickness=1,
    highlightbackground="#2e2e2e",  # Match the background to remove shadow effect
    highlightcolor="#2e2e2e"
)

speedlabel = tk.Label(
    text="Speed",
    font=("Arial", 14),
    bg="#1e1e1e",
    fg="lightgray"
)

# Custom slider using Canvas
canvas = tk.Canvas(window, width=300, height=50, bg="#1e1e1e", highlightthickness=0)
canvas.create_line(20, 20, 280, 20, width=4, fill="#575757")  # Track
knob = canvas.create_oval(20 - 10, 10, 20 + 10, 30, fill="lightgray", outline="")  # Slider knob
canvas.bind("<B1-Motion>", move_slider)

# Slider value
slider_value = tk.IntVar(value=1)

# Buttons
button_frame = tk.Frame(window, bg="#1e1e1e")
submit = tk.Button(
    button_frame,
    text="Start",
    command=type,
    bg="#3DDC97",
    fg="white",
    activebackground="#2AB68E",
    activeforeground="white",
    font=("Arial", 12),
    relief="flat",
    padx=20,
    pady=10,
    highlightthickness=0,
    bd=0,
    borderwidth=0
)
submit.config(width=12, height=1)
submit.configure(highlightbackground="#3DDC97", highlightthickness=0)
submit.configure(borderwidth=0, relief="flat", highlightbackground="#3DDC97")
submit.update()
submit.place(relx=0.5, anchor="center")

stop = tk.Button(
    button_frame,
    text="Stop",
    command=stop_typing,
    bg="#FF6B6B",
    fg="white",
    activebackground="#FF4C4C",
    activeforeground="white",
    font=("Arial", 12),
    relief="flat",
    padx=20,
    pady=10,
    highlightthickness=0,
    bd=0
)
stop.config(width=12, height=1)
stop.update()
stop.place(relx=0.5, anchor="center")

clear_button = tk.Button(
    window,
    text="Clear",
    command=clear_entry,
    bg="#2e2e2e",
    fg="lightgray",
    activebackground="#575757",
    activeforeground="white",
    font=("Arial", 10),
    relief="flat",
    padx=5,
    pady=2,
    highlightthickness=0,
    bd=0
)

# Status Label
status_label = tk.Label(
    text="",
    font=("Arial", 14),
    bg="#1e1e1e",
    fg="lightgray"
)

# Build Window
title.pack(pady=10)
entry.pack(pady=10)
speedlabel.pack(pady=10)
canvas.pack(pady=10)
button_frame.pack(pady=10)
submit.pack(side=tk.LEFT, padx=10)
stop.pack(side=tk.LEFT, padx=10)
status_label.pack(pady=10)
clear_button.pack(pady=5, anchor="w", after=entry)

# Run Application
window.mainloop()
