import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from connect import get_database_connection

def fetch_document_details(case_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM document WHERE CASE_ID = %s", (case_id,))
        documents = cursor.fetchall()
        return documents
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()

def display_document_details():
    case_id = case_id_entry.get()
    if not case_id:
        messagebox.showerror("Error", "Please enter a case ID.")
        return
    documents = fetch_document_details(case_id)
    if documents:
        document_text.delete(1.0, tk.END)
        for document in documents:
            document_id = document["DOCUMENT_ID"]
            content = document["CONTENT"]
            document_type = document["TYPE"]
            submission_date = document["SUBMISSION_DATE"]
            document_text.insert(tk.END, f"Document ID: {document_id}\n")
            document_text.insert(tk.END, f"Content: {content}\n")
            document_text.insert(tk.END, f"Type: {document_type}\n")
            document_text.insert(tk.END, f"Submission Date: {submission_date}\n\n")
    else:
        document_text.delete(1.0, tk.END)
        document_text.insert(tk.END, "No documents found for this case.")

def submit_new_document():
    case_id = case_id_entry.get()
    if not case_id:
        messagebox.showerror("Error", "Please enter a case ID.")
        return
    os.system("python doc2.py")

def back_to_lawyer_home():
    root.destroy()
    os.system("python lawyerhome.py")

# Create the main window
root = tk.Tk()
root.title("Documents")
root.geometry("1000x700")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((200, 200), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Documents", font=("Arial", 20))
heading_label.pack(pady=10)

# Entry for Case ID
case_id_label = tk.Label(root, text="Enter Case ID:")
case_id_label.pack()
case_id_entry = tk.Entry(root)
case_id_entry.pack(pady=5)

# Button to display document details
display_button = tk.Button(root, text="Display Document Details", command=display_document_details)
display_button.pack(pady=10)

# Button to submit new document
submit_button = tk.Button(root, text="Submit New Document", command=submit_new_document)
submit_button.pack(pady=10)

# Document text area
document_text = tk.Text(root, height=10, width=60)
document_text.pack(pady=10)

# Back button to lawyer home
back_button = tk.Button(root, text="Back", command=back_to_lawyer_home)
back_button.pack(pady=10)

root.mainloop()
