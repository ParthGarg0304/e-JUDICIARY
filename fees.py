import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import mysql.connector
from connect import get_database_connection
from decimal import Decimal

def fetch_case_title(case_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT TITLE FROM `case` WHERE CASE_ID = %s", (case_id,))
        result = cursor.fetchone()
        if result:
            return result["TITLE"]
        else:
            messagebox.showerror("Error", "Case not found.")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()

def fetch_fees_status(case_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT STATUS FROM legal_fees WHERE CASE_ID = %s", (case_id,))
        result = cursor.fetchone()
        if result:
            return result["STATUS"]
        else:
            return "Not Available"
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()

def fetch_penalty_amount(case_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT penalty FROM legal_fees WHERE CASE_ID = %s", (case_id,))
        result = cursor.fetchone()
        if result:
            return result["penalty"]
        else:
            return 0.00
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()

def update_fees(case_id, amount):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT AMOUNT FROM legal_fees WHERE CASE_ID = %s", (case_id,))
        result = cursor.fetchone()
        if result:
            remaining_amount = result["AMOUNT"] - Decimal(amount)  # Convert amount to Decimal
            if remaining_amount < 0:
                messagebox.showerror("Error", "Entered amount exceeds the remaining fees.")
                return
            elif remaining_amount == 0:
                status = "Paid"
            else:
                status = "Pending"
            cursor.execute("UPDATE legal_fees SET AMOUNT = %s, STATUS = %s WHERE CASE_ID = %s",
                           (remaining_amount, status, case_id))
            db.commit()
            messagebox.showinfo("Success", "Fees updated successfully.")
        else:
            messagebox.showerror("Error", "Case not found in legal fees table.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        if db:
            db.close()

def display_case_details():
    case_id = case_id_entry.get()
    if not case_id:
        messagebox.showerror("Error", "Please enter a case ID.")
        return
    case_title = fetch_case_title(case_id)
    if case_title:
        case_title_label.config(text=f"Case Title: {case_title}")
        fees_status = fetch_fees_status(case_id)
        fees_status_label.config(text=f"Fees Status: {fees_status}")
        penalty_amount = fetch_penalty_amount(case_id)
        penalty_label.config(text=f"Penalty Amount: {penalty_amount}")

def update_fees_amount():
    case_id = case_id_entry.get()
    amount = amount_entry.get()
    if not case_id:
        messagebox.showerror("Error", "Please enter a case ID.")
        return
    if not amount:
        messagebox.showerror("Error", "Please enter the amount to be paid.")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return
    update_fees(case_id, amount)

def back_to_client_home():
    root.destroy()
    os.system("python clienthome.py")

# Create the main window
root = tk.Tk()
root.title("Legal Fees")
root.geometry("1000x700")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((200, 200), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Legal Fees", font=("Arial", 20))
heading_label.pack(pady=10)

# Entry for Case ID
case_id_label = tk.Label(root, text="Enter Case ID:")
case_id_label.pack()
case_id_entry = tk.Entry(root)
case_id_entry.pack(pady=5)

# Display Case Title
case_title_label = tk.Label(root, text="")
case_title_label.pack(pady=5)

# Display Fees Status
fees_status_label = tk.Label(root, text="")
fees_status_label.pack(pady=5)

# Display Penalty Amount
penalty_label = tk.Label(root, text="")
penalty_label.pack(pady=5)

# Entry for Amount to be paid
amount_label = tk.Label(root, text="Enter Amount to be Paid:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

# Display button to show case details
display_button = tk.Button(root, text="Display Case Details", command=display_case_details)
display_button.pack(pady=10)

# Button to update fees amount
update_button = tk.Button(root, text="Update Fees Amount", command=update_fees_amount)
update_button.pack(pady=10)

# Back button to client home
back_button = tk.Button(root, text="Back", command=back_to_client_home)
back_button.pack(pady=10)

root.mainloop()
