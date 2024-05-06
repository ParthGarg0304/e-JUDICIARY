import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from connect import get_database_connection


def fetch_notifications(user_id):
    try:
        db = get_database_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notification WHERE USER_ID = %s", (user_id,))
        notifications = cursor.fetchall()
        return notifications
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return None
    finally:
        if db:
            db.close()


def display_notifications():
    user_id = user_id_entry.get()
    if not user_id:
        messagebox.showerror("Error", "Please enter a user ID.")
        return
    notifications = fetch_notifications(user_id)
    if notifications:
        notification_text.delete(1.0, tk.END)
        for notification in notifications:
            notification_id = notification["NOTIFICATION_ID"]
            status = notification["STATUS"]
            date = notification["DATE"]
            message = notification["MESSAGE"]
            detail_sent = notification["DETAIL_SENT"]
            notification_text.insert(tk.END, f"Notification ID: {notification_id}\n")
            notification_text.insert(tk.END, f"Status: {status}\n")
            notification_text.insert(tk.END, f"Date: {date}\n")
            notification_text.insert(tk.END, f"Message: {message}\n")
            notification_text.insert(tk.END, f"Detail Sent: {detail_sent}\n\n")
    else:
        notification_text.delete(1.0, tk.END)
        notification_text.insert(tk.END, "No notifications found for this user.")


def back_to_client_home():
    root.destroy()
    os.system("python clienthome.py")


# Create the main window
root = tk.Tk()
root.title("Notifications")
root.geometry("1000x700")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((200, 200), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Legal Fees", font=("Arial", 20))
heading_label.pack(pady=10)

# Entry for User ID
user_id_label = tk.Label(root, text="Enter User ID:")
user_id_label.pack()
user_id_entry = tk.Entry(root)
user_id_entry.pack(pady=5)

# Button to display notifications
display_button = tk.Button(root, text="Display Notifications", command=display_notifications)
display_button.pack(pady=10)

# Notification text area
notification_text = tk.Text(root, height=10, width=60)
notification_text.pack(pady=10)

# Back button to client home
back_button = tk.Button(root, text="Back", command=back_to_client_home)
back_button.pack(pady=10)

root.mainloop()
