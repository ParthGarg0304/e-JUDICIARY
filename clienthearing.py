import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import mysql.connector
from connect import get_database_connection

def fetch_case_title(case_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT TITLE FROM `case` WHERE CASE_ID = %s", (case_id,))
        result = cursor.fetchone()
        return result["TITLE"] if result else None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()

def fetch_schedule_details(case_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM schedule WHERE CASE_ID = %s", (case_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()

def fetch_court_details(court_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM court WHERE COURT_ID = %s", (court_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()

def display_upcoming_hearing():
    case_id = case_id_entry.get()
    if not case_id:
        messagebox.showerror("Error", "Please enter a case ID.")
        return
    case_title = fetch_case_title(case_id)
    if case_title:
        case_title_label.config(text=f"Case Title: {case_title}")
        schedule_details = fetch_schedule_details(case_id)
        if schedule_details:
            hearing_date_label.config(text=f"Hearing Date: {schedule_details['HEARING_DATE']}")
            agenda_label.config(text=f"Agenda: {schedule_details['AGENDA']}")
            court_id = schedule_details['COURT_ID']
            court_details = fetch_court_details(court_id)
            if court_details:
                court_name_label.config(text=f"Court Name: {court_details['NAME']}")
                court_type_label.config(text=f"Court Type: {court_details['TYPE']}")
                location_label.config(text=f"Location: {court_details['LOCATION']}")
        else:
            messagebox.showerror("Error", "No upcoming hearing found for this case.")
    else:
        messagebox.showerror("Error", "Invalid case ID.")

def back_to_client_home():
    root.destroy()
    os.system("python clienthome.py")

# Create the main window
root = tk.Tk()
root.title("Upcoming Hearing")
root.geometry("1000x700")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((200, 200), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Upcoming Hearing", font=("Arial", 20))
heading_label.pack(pady=10)

# Entry for Case ID
case_id_label = tk.Label(root, text="Enter Case ID:")
case_id_label.pack()
case_id_entry = tk.Entry(root)
case_id_entry.pack(pady=5)

# Display Case Title
case_title_label = tk.Label(root, text="")
case_title_label.pack(pady=5)

# Display Hearing Date
hearing_date_label = tk.Label(root, text="")
hearing_date_label.pack(pady=5)

# Display Agenda
agenda_label = tk.Label(root, text="")
agenda_label.pack(pady=5)

# Display Court Name
court_name_label = tk.Label(root, text="")
court_name_label.pack(pady=5)

# Display Court Type
court_type_label = tk.Label(root, text="")
court_type_label.pack(pady=5)

# Display Location
location_label = tk.Label(root, text="")
location_label.pack(pady=5)

# Display button to show upcoming hearing details
display_button = tk.Button(root, text="Display Upcoming Hearing", command=display_upcoming_hearing)
display_button.pack(pady=10)

# Back button to client home
back_button = tk.Button(root, text="Back", command=back_to_client_home)
back_button.pack(pady=10)

root.mainloop()
