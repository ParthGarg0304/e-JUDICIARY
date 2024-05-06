import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from connect import get_database_connection
from datetime import date

def update_document(case_id, content, document_type):
    db = None
    try:
        db = get_database_connection()
        cursor = db.cursor()
        submission_date = date.today()
        cursor.execute("INSERT INTO document (CASE_ID, CONTENT, TYPE, SUBMISSION_DATE) VALUES (%s, %s, %s, %s)",
                       (case_id, content, document_type, submission_date))
        db.commit()
        messagebox.showinfo("Success", "Document submitted successfully!")
        back_to_doc()  # Call this here if you want automatic redirection after successful submission
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        if db:
            db.close()

def back_to_doc():
    root.destroy()
    os.system("python doc.py")

# Create the main window
root = tk.Tk()
root.title("Submit New Document")
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

# Text widget for Document Content
content_label = tk.Label(root, text="Enter Document Content:")
content_label.pack()
content_text = tk.Text(root, height=10, width=50)
content_text.pack(pady=5)

# Entry for Document Type
type_label = tk.Label(root, text="Enter Document Type:")
type_label.pack()
type_entry = tk.Entry(root)
type_entry.pack(pady=5)

# Button to submit new document
submit_button = tk.Button(root, text="Submit Document", command=lambda: update_document(case_id_entry.get(), content_text.get("1.0", tk.END), type_entry.get()))
submit_button.pack(pady=10)

# Back button to doc.py
back_button = tk.Button(root, text="Back", command=back_to_doc)
back_button.pack(pady=10)

root.mainloop()
