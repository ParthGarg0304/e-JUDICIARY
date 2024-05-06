import tkinter as tk
from tkinter import ttk
import os

# Create Tkinter window
root = tk.Tk()
root.title("Home Page")
root.geometry("1000x600")

# Load image
image = tk.PhotoImage(file="court.png")

# Header with image
header_label = tk.Label(root, image=image)
header_label.pack(pady=20)

# Create a frame for buttons
buttons_frame = ttk.Frame(root)
buttons_frame.pack(pady=20)

# Button labels
button_labels = [
    ("Case Status", "clientstatus.py"),
    ("Legal Fees", "fees.py"),
    ("Upcoming Hearing", "clienthearing.py"),
    ("Notifications", "clientnotification.py"),
    ("Update Password", "updatepass.py")
]

# Function to handle button clicks
def button_click(script_name):
    os.system(f"python {script_name}")

# Create buttons and align them in two columns
for i, (label, script) in enumerate(button_labels):
    row = i // 2
    column = i % 2
    button = ttk.Button(buttons_frame, text=label, command=lambda script=script: button_click(script))
    button.grid(row=row, column=column, padx=10, pady=10)

# Logout button
def logout():
    root.destroy()
    os.system("python login.py")

logout_button = ttk.Button(root, text="Logout", command=logout)
logout_button.pack(side=tk.BOTTOM, pady=20)

# Start Tkinter event loop
root.mainloop()
