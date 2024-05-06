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

# Button labels and respective file names
button_data = [
    ("Case Status", "lawyerstatus.py"),
    ("Documents", "doc.py"),
    ("Request Schedule", "schedule.py"),
    ("Add Case", "addcase.py"),
    ("Upcoming Hearing", "lawyerhearing.py"),
    ("Notifications", "lawyernotification.py"),
    ("Update Password", "updatepass.py")
]

# Function to handle button clicks
def button_click(filename):
    os.system("python " + filename)

# Create buttons and align them in two columns
for i, (label, filename) in enumerate(button_data):
    row = i // 2
    column = i % 2
    button = ttk.Button(buttons_frame, text=label, command=lambda filename=filename: button_click(filename))
    button.grid(row=row, column=column, padx=10, pady=10)

# Logout button
def logout():
    root.destroy()
    os.system("python login.py")

logout_button = ttk.Button(root, text="Logout", command=logout)
logout_button.pack(side=tk.BOTTOM, pady=20)

# Start Tkinter event loop
root.mainloop()
