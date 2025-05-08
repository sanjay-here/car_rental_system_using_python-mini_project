import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
from PIL import Image, ImageTk  # Import Pillow for image handling

# Declare tree and root as global variables
tree = None
root = None

# Predefined admin password
ADMIN_PASSWORD = "admin123"  # Change this to your desired password
UPDATED_BOOKINGS_FILE = "updated_bookings.json"  # File where updated data will be saved

def insert_current_date():
    selected_items = tree.selection()
    if selected_items:
        current_date = datetime.now().strftime("%Y-%m-%d")
        for item in selected_items:
            tree.set(item, column="pickup_date", value=current_date)

def on_double_click(event):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    
    if column == "#6":  # "Confirmation" column
        edit_cell_with_dropdown(item, column, ["Confirmed", "Not Confirmed"])
    elif column == "#7":  # "Pick-up Date" column
        edit_cell_with_entry(item, column)
    elif column == "#8":  # "Payment Status" column
        edit_cell_with_dropdown(item, column, ["Paid", "Not Paid"])

def edit_cell_with_dropdown(item, column, options):
    x, y, width, height = tree.bbox(item, column)
    combobox = ttk.Combobox(root, values=options, state="readonly")
    
    current_value = tree.item(item, "values")[int(column[1:]) - 1]
    combobox.set(current_value)
    combobox.place(x=x, y=y + height // 2, width=width, anchor="w")
    
    def save_selection(event):
        tree.set(item, column=column, value=combobox.get())
        combobox.destroy()
    
    combobox.bind("<<ComboboxSelected>>", save_selection)

def edit_cell_with_entry(item, column):
    x, y, width, height = tree.bbox(item, column)
    entry = tk.Entry(root)
    
    current_value = tree.item(item, "values")[int(column[1:]) - 1]
    entry.insert(0, current_value)
    entry.place(x=x, y=y + height // 2, width=width, anchor="w")
    
    def save_entry(event):
        tree.set(item, column=column, value=entry.get())
        entry.destroy()

    entry.bind("<Return>", save_entry)  # Save entry when the Enter key is pressed
    entry.focus()

def save_data():
    try:
        updated_data = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            # Prepare the updated data based on the Treeview values
            updated_data.append({
                "username": values[0],
                "car_category": values[1],
                "car": values[2],
                "days": values[3],
                "phone_number": values[4],
                "confirmation": values[5] if values[5] else "Not Confirmed",  # Default if empty
                "pickup_date": values[6] if values[6] else "",  # Default if empty
                "payment_status": values[7] if values[7] else "Not Paid"  # Default if empty
            })

        # Write the updated data to the JSON file
        with open(UPDATED_BOOKINGS_FILE, "w") as file:
            json.dump(updated_data, file, indent=4)

        messagebox.showinfo("Success", "Data saved successfully!")

    except Exception as e:
        print(f"Error saving data: {e}")
        messagebox.showerror("Error", f"Error saving data: {e}")

def load_data():
    # Clear the current Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Read the updated bookings data from updated_bookings.json if it exists
    updated_data = []
    if os.path.exists(UPDATED_BOOKINGS_FILE):
        try:
            with open(UPDATED_BOOKINGS_FILE, "r") as file:
                updated_data = json.load(file)
                print(f"Loaded bookings from {UPDATED_BOOKINGS_FILE}.")  # Debug
        except Exception as e:
            print(f"Error loading data from {UPDATED_BOOKINGS_FILE}: {e}")

    # Read the original bookings data from carbookings.txt
    if os.path.exists("carbookings.txt"):
        try:
            with open("carbookings.txt", "r") as file:
                for line in file:
                    # Safely evaluate the dictionary string
                    booking = eval(line.strip())  # Using eval here for simplicity; consider safer alternatives.
                    # Check if booking already exists in updated_data
                    confirmation = ""
                    pickup_date = ""
                    payment_status = "Not Paid"  # Default payment status

                    # If the booking is already in updated_data, get the additional info
                    for updated_booking in updated_data:
                        if updated_booking["username"] == booking["username"] and updated_booking["car"] == booking["car"]:
                            confirmation = updated_booking.get("confirmation", "")
                            pickup_date = updated_booking.get("pickup_date", "")
                            payment_status = updated_booking.get("payment_status", "Not Paid")
                            break
                    
                    # Insert the booking into the Treeview
                    tree.insert("", tk.END, values=(
                        booking["username"],
                        booking["car_category"],
                        booking["car"],
                        booking["days"],
                        booking["phone_number"],
                        confirmation,  # Added confirmation from updated data if exists
                        pickup_date,   # Added pickup date from updated data if exists
                        payment_status  # Added payment status from updated data if exists
                    ))
                print(f"Loaded bookings from carbookings.txt.")  # Debug
        except Exception as e:
            print(f"Error loading data from carbookings.txt: {e}")


def create_admin_panel():
    global tree, root  # Declare both tree and root as global variables
    
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("1200x500")

    # Create a Frame for the Treeview and Scrollbar
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Add a Scrollbar
    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a Treeview widget
    columns = ("username", "car_category", "car", "days", "phone_number", "confirmation", "pickup_date", "payment_status")
    tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

    # Configure the Scrollbar
    scrollbar.config(command=tree.yview)

    # Define the headings
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())

    # Define the column widths
    tree.column("username", width=100)
    tree.column("car_category", width=100)
    tree.column("car", width=200)
    tree.column("days", width=50)
    tree.column("phone_number", width=120)
    tree.column("confirmation", width=120)
    tree.column("pickup_date", width=120)
    tree.column("payment_status", width=120)

    # Pack the Treeview
    tree.pack(fill=tk.BOTH, expand=True)

    # Create a Save button
    save_button = tk.Button(root, text="Save", command=save_data)
    save_button.pack()

    # Create a button to insert the current date in the selected row
    current_date_button = tk.Button(root, text="Insert Current Date", command=insert_current_date)
    current_date_button.pack()

    # Load the initial data into the Treeview
    load_data()

    # Bind double-click to open dropdown editing
    tree.bind("<Double-1>", on_double_click)

    # Add greeting label
    greeting_label = tk.Label(root, text="Welcome Admin to the Car Rental System", font=("Arial", 14))
    greeting_label.pack(pady=10)

    root.mainloop()

def show_login_window():
    # Create a new Tkinter window for login
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("500x400")

    # Load background image
    background_image = Image.open("adminimg.jpg")  # Use the actual file name
    background_image = background_image.resize((500, 400), Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
    background_image = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(login_window, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Stretch the image to cover the entire window

    def validate_password():
        entered_password = password_entry.get()
        if entered_password == ADMIN_PASSWORD:
            login_window.destroy()  # Close the login window
            create_admin_panel()  # Open the admin panel
        else:
            messagebox.showerror("Login Error", "Incorrect password. Please try again.")

    # Password entry frame for better placement
    frame = tk.Frame(login_window, bg="white", padx=10, pady=10)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    password_label = tk.Label(frame, text="Enter Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(frame, text="Login", command=validate_password)
    login_button.pack(pady=10)

    login_window.mainloop()

# Start the application
show_login_window()
