import tkinter as tk
from tkinter import messagebox
import os
from connect import get_database_connection

# Create Tkinter window
root = tk.Tk()
root.title("Create Account")
root.geometry("1000x600")

# Function to handle create account
def create_account():
    # Get input values
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    dob = dob_entry.get()
    age = age_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone_no = phone_no_entry.get()
    role = role_var.get()
    email = email_entry.get()
    
    # Validate password
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        # Connect to database
        db = get_database_connection()
        cursor = db.cursor()

        # Insert user data into user table
        cursor.execute("INSERT INTO user (USERNAME, DOB, AGE, F_NAME, L_NAME, PHONE_NO, ROLE, EMAIL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, dob, age, first_name, last_name, phone_no, role, email))
        db.commit()
        
        # Get user_id of the newly inserted user
        user_id = cursor.lastrowid
        
        # Insert encrypted password into encrypt table
        cursor.execute("INSERT INTO encrypt (USER_ID, PASSWORD) VALUES (%s, %s)", (user_id, password))
        db.commit()
        
        messagebox.showinfo("Success", "Account created successfully!")
        root.destroy()  # Close create account window
        os.system("python login.py")  # Open login page
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# Create widgets for create account page
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")
confirm_password_label = tk.Label(root, text="Confirm Password:")
confirm_password_entry = tk.Entry(root, show="*")
dob_label = tk.Label(root, text="Date of Birth (YYYY-MM-DD):")
dob_entry = tk.Entry(root)
age_label = tk.Label(root, text="Age:")
age_entry = tk.Entry(root)
first_name_label = tk.Label(root, text="First Name:")
first_name_entry = tk.Entry(root)
last_name_label = tk.Label(root, text="Last Name:")
last_name_entry = tk.Entry(root)
phone_no_label = tk.Label(root, text="Phone Number:")
phone_no_entry = tk.Entry(root)
role_label = tk.Label(root, text="Role:")
role_var = tk.StringVar(value="Client")
role_radiobutton1 = tk.Radiobutton(root, text="Client", variable=role_var, value="Client")
role_radiobutton2 = tk.Radiobutton(root, text="Lawyer", variable=role_var, value="Lawyer")
email_label = tk.Label(root, text="Email:")
email_entry = tk.Entry(root)
create_account_button = tk.Button(root, text="Create Account", command=create_account)

# Arrange widgets using grid layout
username_label.grid(row=0, column=0, pady=5)
username_entry.grid(row=0, column=1, pady=5)
password_label.grid(row=1, column=0, pady=5)
password_entry.grid(row=1, column=1, pady=5)
confirm_password_label.grid(row=2, column=0, pady=5)
confirm_password_entry.grid(row=2, column=1, pady=5)
dob_label.grid(row=3, column=0, pady=5)
dob_entry.grid(row=3, column=1, pady=5)
age_label.grid(row=4, column=0, pady=5)
age_entry.grid(row=4, column=1, pady=5)
first_name_label.grid(row=5, column=0, pady=5)
first_name_entry.grid(row=5, column=1, pady=5)
last_name_label.grid(row=6, column=0, pady=5)
last_name_entry.grid(row=6, column=1, pady=5)
phone_no_label.grid(row=7, column=0, pady=5)
phone_no_entry.grid(row=7, column=1, pady=5)
role_label.grid(row=8, column=0, pady=5)
role_radiobutton1.grid(row=8, column=1, pady=5, padx=(0, 20))
role_radiobutton2.grid(row=8, column=2, pady=5)
email_label.grid(row=9, column=0, pady=5)
email_entry.grid(row=9, column=1, pady=5)
create_account_button.grid(row=10, column=0, columnspan=2, pady=5)

# Center the input fields
for i in range(11):
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start Tkinter event loop
root.mainloop()
