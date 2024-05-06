import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from connect import get_database_connection
from datetime import date, timedelta
import random

def generate_random_date():
    today = date.today()
    three_months_later = today + timedelta(days=random.randint(30, 90))
    return three_months_later

def generate_random_court_id():
    return random.randint(1, 5)

def schedule_hearing(case_id, agenda):
    try:
        db = get_database_connection()
        cursor = db.cursor()
        court_id = generate_random_court_id()
        hearing_date = generate_random_date()
        cursor.execute("INSERT INTO schedule (COURT_ID, HEARING_DATE, AGENDA, CASE_ID) VALUES (%s, %s, %s, %s)", (court_id, hearing_date, agenda, case_id))
        db.commit()
        messagebox.showinfo("Success", "Hearing scheduled successfully!")
        return court_id, hearing_date
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None, None
    finally:
        if db:
            db.close()

def display_schedule_details(case_id, agenda):
    court_id, hearing_date = schedule_hearing(case_id, agenda)
    if court_id and hearing_date:
        messagebox.showinfo("Schedule Details", f"Court ID: {court_id}\nHearing Date: {hearing_date}")
    else:
        messagebox.showerror("Error", "Failed to schedule hearing. Please try again.")

def back_to_lawyer_home():
    root.destroy()
    os.system("python lawyerhome.py")

# Create the main window
root = tk.Tk()
root.title("Request Hearing Schedule")
root.geometry("1000x700")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((200, 200), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Request Hearing Schedule", font=("Arial", 20))
heading_label.pack(pady=10)

# Entry for Case ID
case_id_label = tk.Label(root, text="Enter Case ID:")
case_id_label.pack()
case_id_entry = tk.Entry(root)
case_id_entry.pack(pady=5)

# Entry for Agenda
agenda_label = tk.Label(root, text="Enter Agenda:")
agenda_label.pack()
agenda_entry = tk.Entry(root)
agenda_entry.pack(pady=5)

# Button to schedule hearing
schedule_button = tk.Button(root, text="Schedule Hearing", command=lambda: display_schedule_details(case_id_entry.get(), agenda_entry.get()))
schedule_button.pack(pady=10)

# Back button to lawyerhome.py
back_button = tk.Button(root, text="Back", command=back_to_lawyer_home)
back_button.pack(pady=10)

root.mainloop()
