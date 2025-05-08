import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
from PIL import Image, ImageTk

# Load credentials from a JSON file
def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Credentials file not found.")
        return {}

# Save credentials to a JSON file
def save_credentials(credentials):
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)

# Register a new user
def register_user():
    def save_new_user():
        username = entry_new_username.get()
        password = entry_new_password.get()

        if username and password:
            credentials = load_credentials()
            
            if username in credentials:
                messagebox.showerror("Error", "Username already exists.")
            else:
                credentials[username] = password
                save_credentials(credentials)
                messagebox.showinfo("Success", "User registered successfully!")
                register_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill out both fields.")

    # Create registration window
    register_window = tk.Toplevel(login_window)
    register_window.title("Register New User")
    register_window.geometry("400x300")

    tk.Label(register_window, text="Enter New Username:", font=("Arial", 12)).pack(pady=10)
    entry_new_username = tk.Entry(register_window, font=("Arial", 12))
    entry_new_username.pack(pady=5)

    tk.Label(register_window, text="Enter New Password:", font=("Arial", 12)).pack(pady=10)
    entry_new_password = tk.Entry(register_window, show="*", font=("Arial", 12))
    entry_new_password.pack(pady=5)

    tk.Button(register_window, text="Register", font=("Arial", 12), command=save_new_user).pack(pady=20)

# Login function
def login():
    global global_username  # Define global_username at the beginning of the function

    credentials = load_credentials()

    username = entry_username.get()
    password = entry_password.get()

    if username in credentials and credentials[username] == password:
        global_username = username  # Store the logged-in username globally
        main_menu()
    else:
        messagebox.showerror("Error", "Invalid credentials. Try again!")

# Logout function
def logout():
    menu_window.destroy()  # Close the main menu window
    create_login_window()  # Recreate the login window

# Main Menu function
def main_menu():
    login_window.destroy()
    global menu_window
    menu_window = tk.Tk()
    menu_window.title("Main Menu Page")
    menu_window.geometry("800x500")

    # Set background image for menu
    bg_image = Image.open("carim2.jpg")
    bg_image = bg_image.resize((800, 500), Image.LANCZOS)
    bg_photo_menu = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(menu_window, image=bg_photo_menu)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Main Menu Buttons
    tk.Button(menu_window, text="Rent a Car Now", font=("Arial", 16), command=open_category_window).place(x=50, y=100)
    tk.Button(menu_window, text="My Rental History", font=("Arial", 16), command=view_rental_history).place(x=50, y=180)
    tk.Button(menu_window, text="Customer Care", font=("Arial", 16), command=customer_care).place(x=50, y=260)
    tk.Button(menu_window, text="Terms and Conditions", font=("Arial", 16), command=show_terms_and_conditions).place(x=50, y=340)
    tk.Button(menu_window, text="Logout", font=("Arial", 16), command=logout).place(x=680, y=20)

    menu_window.mainloop()

# Function to show the login window
def show_login_window():
    login_window.deiconify()  # Show the login window again

def open_category_window():
    category_window = tk.Toplevel(menu_window)
    category_window.title("Car Categories")
    category_window.geometry("800x500")

    # Set background image for category window
    bg_image = Image.open("carim3.jpg")
    bg_image = bg_image.resize((800, 500), Image.LANCZOS)
    bg_photo_category = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(category_window, image=bg_photo_category)
    bg_label.image = bg_photo_category  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(category_window, text="Select Car Category:", font=("Arial", 16), bg="white").pack(pady=20)

    tk.Button(category_window, text="Sedan", font=("Arial", 14), command=lambda: show_sedan_cars("Sedan")).pack(pady=10)
    tk.Button(category_window, text="SUV", font=("Arial", 14), command=lambda: show_suv_cars("SUV")).pack(pady=10)
    tk.Button(category_window, text="Hatchback", font=("Arial", 14), command=lambda: show_hatchback_cars("Hatchback")).pack(pady=10)

    tk.Button(category_window, text="Back to Menu", font=("Arial", 14), command=category_window.destroy).pack(pady=20)

def show_sedan_cars(category):
    sedan_window = tk.Toplevel(menu_window)
    sedan_window.title("Available Sedan Cars")
    sedan_window.geometry("800x500")

    # Set background image for sedan window
    bg_image = Image.open("sedanimg.jpg")
    bg_image = bg_image.resize((800, 500), Image.LANCZOS)
    bg_photo_sedan = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(sedan_window, image=bg_photo_sedan)
    bg_label.image = bg_photo_sedan  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(sedan_window, text="Available Sedan Cars", font=("Arial", 16), bg="white").pack(pady=10)

    cars = [
        "Volkswagen Virtus - 2000/DAY (Excluding GST)",
        "Skoda Superb - 3500/DAY (Excluding GST)",
        "Audi A6 - 5000/DAY (Excluding GST)"
    ]

    for car in cars:
        frame = tk.Frame(sedan_window, bg="white")
        frame.pack(pady=5)

        tk.Label(frame, text=car, font=("Arial", 14), bg="white").pack(side=tk.LEFT, padx=10)

        days_var = tk.IntVar(value=1)
        tk.Label(frame, text="Days:", bg="white").pack(side=tk.LEFT, padx=5)
        tk.Spinbox(frame, from_=1, to=10, textvariable=days_var, width=5).pack(side=tk.LEFT)

        tk.Button(frame, text="Request Booking", command=lambda c=car, d=days_var: request_booking(c, d.get(), category)).pack(side=tk.LEFT, padx=10)

def show_suv_cars(category):
    suv_window = tk.Toplevel(menu_window)
    suv_window.title("Available SUV Cars")
    suv_window.geometry("800x500")

    # Set background image for SUV window
    bg_image = Image.open("suvimg.jpg")
    bg_image = bg_image.resize((800, 500), Image.LANCZOS)
    bg_photo_suv = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(suv_window, image=bg_photo_suv)
    bg_label.image = bg_photo_suv  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(suv_window, text="Available SUV Cars", font=("Arial", 16), bg="white").pack(pady=10)

    suvs = [
        "Mahindra THAR 4X4 - 3000/DAY (Excluding GST)",
        "TATA HARRIER - 4000/DAY (Excluding GST)",
        "BMW X5 - 6000/DAY (Excluding GST)"
    ]

    for suv in suvs:
        frame = tk.Frame(suv_window, bg="white")
        frame.pack(pady=5)

        tk.Label(frame, text=suv, font=("Arial", 14), bg="white").pack(side=tk.LEFT, padx=10)

        days_var = tk.IntVar(value=1)
        tk.Label(frame, text="Days:", bg="white").pack(side=tk.LEFT, padx=5)
        tk.Spinbox(frame, from_=1, to=10, textvariable=days_var, width=5).pack(side=tk.LEFT)

        tk.Button(frame, text="Request Booking", command=lambda c=suv, d=days_var: request_booking(c, d.get(), category)).pack(side=tk.LEFT, padx=10)

def show_hatchback_cars(category):
    try:
        hatchback_window = tk.Toplevel(menu_window)
        hatchback_window.title("Available Hatchback Cars")
        hatchback_window.geometry("800x500")

        # Set background image for hatchback window
        bg_image = Image.open("hatchimg.jpg")
        bg_image = bg_image.resize((800, 500), Image.LANCZOS)
        bg_photo_hatchback = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(hatchback_window, image=bg_photo_hatchback)
        bg_label.image = bg_photo_hatchback  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(hatchback_window, text="Available Hatchback Cars", font=("Arial", 16), bg="white").pack(pady=10)

        hatchbacks = [
            "Maruti Suzuki Swift - 1500/DAY (Excluding GST)",
            "Volkswagen Polo GT - 3000/DAY (Excluding GST)",
            "Mini Cooper Countryman - 6000/DAY (Excluding GST)"
        ]

        for hatchback in hatchbacks:
            frame = tk.Frame(hatchback_window, bg="white")
            frame.pack(pady=5)

            tk.Label(frame, text=hatchback, font=("Arial", 14), bg="white").pack(side=tk.LEFT, padx=10)

            days_var = tk.IntVar(value=1)
            tk.Label(frame, text="Days:", bg="white").pack(side=tk.LEFT, padx=5)
            tk.Spinbox(frame, from_=1, to=10, textvariable=days_var, width=5).pack(side=tk.LEFT)

            tk.Button(frame, text="Request Booking", command=lambda c=hatchback, d=days_var: request_booking(c, d.get(), category)).pack(side=tk.LEFT, padx=10)

    except Exception as e:
        print(f"Error in show_hatchback_cars: {e}")  # Print error message
        messagebox.showerror("Error", f"An error occurred while loading hatchback cars: {e}")

def request_booking(car, days, car_category):
    global global_username

    # Prompt the user for a phone number
    try:
        phone_number = simpledialog.askstring("Phone Number", "Please enter your phone number:")
        
        # Ensure the dialog was successfully completed
        if not phone_number:
            messagebox.showerror("Error", "Phone number is required.")
            return
        
        # Construct booking details
        booking_details = {
            "username": global_username,
            "car_category": car_category,
            "car": car,
            "days": days,
            "phone_number": phone_number
        }

        # Save booking details to a text file
        with open("carbookings.txt", "a") as file:
            file.write(f"{booking_details}\n")

        # Optionally save booking details to a JSON file
        try:
            # Read existing bookings, if the file is empty or not in JSON format, initialize to an empty list
            with open("bookings.json", "r") as json_file:
                try:
                    bookings = json.load(json_file)
                except json.JSONDecodeError:
                    bookings = []

        except FileNotFoundError:
            bookings = []

        # Append the new booking details
        bookings.append(booking_details)

        with open("bookings.json", "w") as json_file:
            json.dump(bookings, json_file)

        # Display the confirmation message with booking details
        messagebox.showinfo(
            "Booking Confirmed",
            f"You have successfully booked {car} for {days} day(s).\n"
            "Our team will contact you soon for payment and scheduling details.\n"
            "Thank you, and Happy Journey!"
        )

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


import tkinter as tk
import json

def view_rental_history():
    global global_username

    # Try to read the booking history from the JSON file
    try:
        with open("bookings.json", "r") as file:
            try:
                bookings = json.load(file)
            except json.JSONDecodeError:
                bookings = []
    except FileNotFoundError:
        bookings = []

    # Filter bookings for the current user
    user_bookings = [booking for booking in bookings if booking['username'] == global_username]

    # Create a new window to display booking history
    history_window = tk.Toplevel(menu_window)
    history_window.title("My Rental History")
    history_window.geometry("800x500")

    # Set up a scrollable frame in case of many bookings
    scroll_frame = tk.Frame(history_window)
    scroll_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(scroll_frame)
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Display user's bookings
    if user_bookings:
        tk.Label(scrollable_frame, text="Your Rental History:", font=("Arial", 16)).pack(pady=10)
        for booking in user_bookings:
            tk.Label(
                scrollable_frame,
                text=f"Car Category: {booking['car_category']}\nCar: {booking['car']}\nDays: {booking['days']}\nPhone Number: {booking['phone_number']}\n",
                font=("Arial", 14),
                justify="left",
                relief="solid",
                padx=10,
                pady=5
            ).pack(pady=5, fill="x")
        
        # Scroll to the bottom of the canvas
        canvas.yview_moveto(1.0)  # Scroll to the bottom
    else:
        tk.Label(scrollable_frame, text="No rental history found.", font=("Arial", 16)).pack(pady=20)
        # Scroll to the bottom even if no bookings are found
        canvas.yview_moveto(1.0)  # Scroll to the bottom


def customer_care():
    # Create a new window for Customer Care
    care_window = tk.Toplevel(menu_window)
    care_window.title("Customer Care")
    care_window.geometry("400x300")

    # Create a frame for better organization
    care_frame = tk.Frame(care_window, bg="white")
    care_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    tk.Label(care_frame, text="Customer Care", font=("Arial", 20), bg="white").pack(pady=10)

    tk.Label(care_frame, text="Reach Us:", font=("Arial", 16), bg="white").pack(pady=5)

    contact_details = [
        "Phone: +91 1234567890",
        "Email: carrentalsystem@gmail.com"
    ]

    for detail in contact_details:
        tk.Label(care_frame, text=detail, font=("Arial", 14), bg="white").pack(pady=2)

    tk.Button(care_frame, text="Close", command=care_window.destroy).pack(pady=20)

# Function to show terms and conditions
def show_terms_and_conditions():
    terms_window = tk.Toplevel(menu_window)
    terms_window.title("Car Rental System Terms and Conditions")
    terms_window.geometry("800x500")

    # Create a frame for the scrollable area
    frame = tk.Frame(terms_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas and a scrollbar
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(scrollable_frame, text="Car Rental System Terms and Conditions", font=("Arial", 16)).pack(pady=10)

    terms_text = (
        "Here are some basic terms and conditions for an entry-level car rental system:\n\n"
        "1. Rental Duration and Fees:\n"
        "   - The rental fee is based on a daily rate.\n"
        "   - For each additional day beyond the agreed rental period, an extra charge of INR 500 per day will apply.\n"
        "   - Rent is calculated from the date and time of pickup until the vehicle is returned.\n\n"
        "2. Security Deposit:\n"
        "   - A refundable security deposit must be paid at the time of rental.\n"
        "   - The deposit will be returned upon the car's return, provided there are no damages or policy violations.\n\n"
        "3. Fuel Policy:\n"
        "   - The vehicle is rented with a full tank of fuel and should be returned with a full tank.\n"
        "   - If the car is returned with less fuel, a refueling charge, along with a service fee, will apply.\n\n"
        "4. Driver's License and Age:\n"
        "   - All renters must hold a valid driver's license and be at least 21 years old.\n"
        "   - Copies of the driver's license and ID proof must be submitted at the time of booking.\n\n"
        "5. Insurance and Liability:\n"
        "   - The car rental includes basic insurance coverage, which covers third-party damage.\n"
        "   - Any damage to the rented vehicle beyond standard insurance coverage will be the renter's responsibility.\n\n"
        "6. Damage and Maintenance:\n"
        "   - The renter is responsible for any damage to the vehicle during the rental period.\n"
        "   - Regular maintenance costs (e.g., oil changes, tire wear) are the rental company’s responsibility.\n\n"
        "7. Breakdown and Assistance:\n"
        "   - In case of a breakdown, the renter must contact the rental company immediately for assistance.\n"
        "   - Unauthorized repairs are not allowed; the renter will bear costs for repairs not approved by the company.\n\n"
        "8. Traffic Violations and Fines:\n"
        "   - The renter is responsible for any traffic violations or fines incurred during the rental period.\n\n"
        "9. Cancellation Policy:\n"
        "   - Cancellations made 24 hours before the booking are eligible for a full refund.\n"
        "   - Late cancellations may incur a fee.\n\n"
        "10. Late Return:\n"
        "    - A grace period of 1 hour is allowed for returning the vehicle. Beyond that, the daily extra charge applies."
    )
    
    terms_label = tk.Label(scrollable_frame, text=terms_text, justify="left", font=("Arial", 12))
    terms_label.pack(pady=10, padx=10)

    tk.Button(terms_window, text="Close", command=terms_window.destroy).pack(pady=20)
def create_login_window():
    global login_window, entry_username, entry_password
    login_window = tk.Tk()
    login_window.title("Car Rental System Login")
    login_window.geometry("800x500")

    # Set background image for login window
    bg_image = Image.open("carim1.jpg")
    bg_image = bg_image.resize((800, 500), Image.LANCZOS)
    bg_photo_login = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(login_window, image=bg_photo_login)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(login_window, text="Enter Username:", font=("Arial", 16), bg="white").pack(pady=10)
    entry_username = tk.Entry(login_window, font=("Arial", 16))
    entry_username.pack(pady=5)

    tk.Label(login_window, text="Enter Password:", font=("Arial", 16), bg="white").pack(pady=10)
    entry_password = tk.Entry(login_window, show="*", font=("Arial", 16))
    entry_password.pack(pady=5)

    tk.Button(login_window, text="Login", font=("Arial", 16), command=login).pack(pady=20)
    tk.Button(login_window, text="Register New User", font=("Arial", 16), command=register_user).pack(pady=10)

    login_window.mainloop()

# Run the program by creating the login window
create_login_window()
