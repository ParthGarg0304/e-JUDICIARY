import tkinter as tk
from tkinter import messagebox
import os
import random
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from connect import get_database_connection  # Importing the get_database_connection function from connect.py

def submit_case():
    user_id = user_id_entry.get()
    case_name = case_name_entry.get()
    case_description = description_entry.get()
    
    if not all([user_id, case_name, case_description]):
        messagebox.showerror("Error", "All fields are required.")
        return

    # Generate the current date for filing_date
    filing_date = datetime.now().date()

    # Database logic to add a case
    try:
        db = get_database_connection()  # Using the get_database_connection function from connect.py
        cursor = db.cursor()
        
        # Insert into case table
        cursor.execute("INSERT INTO `case` (user_id, filing_date, title, description, status) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, filing_date, case_name, case_description, 'application review'))
        case_id = cursor.lastrowid
        
        db.commit()
        messagebox.showinfo("Success", "New case added successfully. Schedule hearing for the case.")
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        db.close()

def back_to_home():
    root.destroy()
    os.system("python lawyerhome.py")

# Create the main window
root = tk.Tk()
root.title("Submit New Case")
root.geometry("1000x600")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((200, 200), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Submit New Case", font=("Arial", 24))
heading_label.pack(pady=10)

# Entry for User ID
user_id_label = tk.Label(root, text="User ID:")
user_id_label.pack()
user_id_entry = tk.Entry(root)
user_id_entry.pack(pady=5)

# Entry for Case Name
case_name_label = tk.Label(root, text="Case Name:")
case_name_label.pack()
case_name_entry = tk.Entry(root)
case_name_entry.pack(pady=5)

# Entry for Description
description_label = tk.Label(root, text="Description:")
description_label.pack()
description_entry = tk.Entry(root)
description_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit Case", command=submit_case)
submit_button.pack(pady=20)

# Back button
back_button = tk.Button(root, text="Back", command=back_to_home)
back_button.pack()

root.mainloop()
