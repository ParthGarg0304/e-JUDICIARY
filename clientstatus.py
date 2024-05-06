import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from connect import get_database_connection

# Function to retrieve case details based on case ID
def get_case_details(case_id):
    try:
        db = get_database_connection()  # Get database connection
        cursor = db.cursor(dictionary=True)  # Use dictionary cursor

        # Retrieve case details from the case table
        cursor.execute("SELECT * FROM `case` WHERE CASE_ID = %s", (case_id,))
        case_details = cursor.fetchone()

        if not case_details:
            messagebox.showerror("Error", "Case not found.")
            return None

        # Retrieve fees status from the legal_fees table
        cursor.execute("SELECT STATUS FROM legal_fees WHERE CASE_ID = %s", (case_id,))
        fees_status = cursor.fetchone()

        # Combine all details into a single dictionary
        case_data = {
            "applicant_ID": case_details["USER_ID"],  # Assuming USER_ID corresponds to applicant name
            "title": case_details["TITLE"],
            "description": case_details["DESCRIPTION"],
            "status": case_details["STATUS"],
            "filing_date": case_details["FILING_DATE"],
            "fees_status": fees_status["STATUS"] if fees_status else "Not Available",
        }

        return case_data
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
    finally:
        # Close database connection
        if db:
            db.close()

# Function to display case status
def display_case_status():
    case_id = case_id_entry.get()
    if not case_id:
        messagebox.showerror("Error", "Please enter a case ID.")
        return

    try:
        # Retrieve case details based on case ID
        case_details = get_case_details(case_id)

        if case_details:
            # Display case details
            applicant_name_label.config(text=f"Applicant ID: {case_details['applicant_ID']}")
            title_label.config(text=f"Title: {case_details['title']}")
            description_label.config(text=f"Description: {case_details['description']}")
            status_label.config(text=f"Status: {case_details['status']}")
            filing_date_label.config(text=f"Filing Date: {case_details['filing_date']}")
            fees_status_label.config(text=f"Fees Status: {case_details['fees_status']}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def back_to_home():
    root.destroy()
    os.system("python clienthome.py")

# Create the main window
root = tk.Tk()
root.title("Case Status")
root.geometry("1000x700")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((200, 200), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Case Status", font=("Arial", 24))
heading_label.pack(pady=10)

# Entry for Case ID
case_id_label = tk.Label(root, text="Case ID:")
case_id_label.pack()
case_id_entry = tk.Entry(root)
case_id_entry.pack(pady=5)

# Labels to display case details
applicant_name_label = tk.Label(root, text="")
applicant_name_label.pack(pady=5)

title_label = tk.Label(root, text="")
title_label.pack(pady=5)

description_label = tk.Label(root, text="")
description_label.pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

filing_date_label = tk.Label(root, text="")
filing_date_label.pack(pady=5)

fees_status_label = tk.Label(root, text="")
fees_status_label.pack(pady=5)

document_status_label = tk.Label(root, text="")
document_status_label.pack(pady=5)

# Display button
display_button = tk.Button(root, text="Display Case Status", command=display_case_status)
display_button.pack(pady=20)

# Back button
back_button = tk.Button(root, text="Back", command=back_to_home)
back_button.pack()

root.mainloop()
