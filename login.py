import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from connect import get_database_connection, get_database_cursor

# Create Tkinter window
root = tk.Tk()
root.title("Login")
root.geometry("1000x600")

# Load image
image = Image.open("court.png")
image = image.resize((100, 100), Image.BICUBIC)
photo = ImageTk.PhotoImage(image)

# Function to handle login
def login():
    db = get_database_connection()
    cursor = get_database_cursor(db)
    username = username_entry.get()
    password = password_entry.get()
    try:
        cursor.execute("SELECT * FROM user WHERE USERNAME = %s", (username,))
        user_data = cursor.fetchone()
        if user_data:
            user_id, role = user_data[0], user_data[7]  # Get the user's role
            cursor.execute("SELECT PASSWORD FROM encrypt WHERE USER_ID = %s", (user_id,))
            encrypted_password = cursor.fetchone()[0]
            if password == encrypted_password:
                messagebox.showinfo("Success", "Login successful!")
                root.destroy()  # Close login window
                if role == "Client":
                    os.system("python clienthome.py")  # Redirect to client home
                elif role == "Lawyer":
                    os.system("python lawyerhome.py")  # Redirect to lawyer home
            else:
                messagebox.showerror("Error", "Incorrect password!")
        else:
            messagebox.showerror("Error", "User not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# Function to navigate to create account page
def create_account_page():
    root.destroy()  # Close login window
    os.system("python createaccount.py")

# Create widgets for login page
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")
login_button = tk.Button(root, text="Login", command=login)
create_account_button = tk.Button(root, text="Create Account", command=create_account_page)

# Create label for image
image_label = tk.Label(root, image=photo)
login_text_label = tk.Label(root, text="Login", font=("Arial", 18))  # Added label for login text

# Place widgets using the place geometry manager
image_label.place(relx=0.5, rely=0.2, anchor="center")
login_text_label.place(relx=0.5, rely=0.3, anchor="center")  # Position login text below the image
username_label.place(relx=0.35, rely=0.4, anchor="center")
username_entry.place(relx=0.65, rely=0.4, anchor="center")
password_label.place(relx=0.35, rely=0.5, anchor="center")
password_entry.place(relx=0.65, rely=0.5, anchor="center")
login_button.place(relx=0.5, rely=0.6, anchor="center")
create_account_button.place(relx=0.5, rely=0.7, anchor="center")

# Start Tkinter event loop
root.mainloop()
