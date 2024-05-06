import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from connect import get_database_connection, get_database_cursor
import os

def verify_and_update_password():
    current_password = current_password_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()
    
    if new_password != confirm_password:
        messagebox.showerror("Error", "New passwords do not match.")
        return
    
    db = get_database_connection()
    cursor = get_database_cursor(db)
    
    try:
        # Fetch user ID based on current password
        cursor.execute("SELECT USER_ID FROM encrypt WHERE PASSWORD = %s", (current_password,))
        user_data = cursor.fetchone()
        if user_data:
            user_id = user_data[0]
            # Proceed to update password since current password is verified
            cursor.execute("UPDATE encrypt SET PASSWORD = %s WHERE USER_ID = %s", (new_password, user_id))
            db.commit()
            messagebox.showinfo("Success", "Password updated successfully. Login required.")
            root.destroy()
            os.system("python login.py")
        else:
            messagebox.showerror("Error", "Current password is incorrect.")
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        db.close()

def exit_to_login():
    root.destroy()
    os.system("python login.py")

# Create Tkinter window
root = tk.Tk()
root.title("Update Password")
root.geometry("1000x600")

# Load and display image
image = Image.open("court.png")
photo = ImageTk.PhotoImage(image.resize((100, 100), Image.BICUBIC))
image_label = tk.Label(root, image=photo)
image_label.pack(pady=20)

# Heading
heading_label = tk.Label(root, text="Update Password", font=('Helvetica', 18, 'bold'))
heading_label.pack(pady=20)

# Create password fields
current_password_label = tk.Label(root, text="Current Password:")
current_password_label.pack()
current_password_entry = tk.Entry(root, show="*")
current_password_entry.pack()

new_password_label = tk.Label(root, text="New Password:")
new_password_label.pack()
new_password_entry = tk.Entry(root, show="*")
new_password_entry.pack()

confirm_password_label = tk.Label(root, text="Confirm New Password:")
confirm_password_label.pack()
confirm_password_entry = tk.Entry(root, show="*")
confirm_password_entry.pack()

# Create buttons
update_button = tk.Button(root, text="Update Password", command=verify_and_update_password)
update_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_to_login)
exit_button.pack(pady=10)

root.mainloop()
