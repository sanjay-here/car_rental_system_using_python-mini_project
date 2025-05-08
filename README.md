# Car Rental System (Python Tkinter + JSON)

A desktop-based Car Rental System built using Python's Tkinter library for the GUI and JSON files for data storage. This system allows customers to book cars and admins to manage vehicle listings and reservations, all through a clean and interactive GUI.

## Features

### Customer:
- GUI-based login and registration
- Browse available cars
- Book a car with date and time details
- View and cancel bookings

### Admin:
- Admin login
- Add, update, or delete cars
- View all bookings made by customers
- Manage car availability

## Technologies Used

- **Language**: Python 3.x
- **GUI**: Tkinter
- **Data Storage**: JSON (for users, cars, and bookings)
- **Modules**: `tkinter`, `json`, `datetime`, `tkinter.messagebox`

## How Data is Stored

Data is saved in `.json` files like:

- `users.json` – stores registered users
- `cars.json` – stores available cars
- `bookings.json` – stores booking details

These files act as a lightweight database for storing and retrieving information.

## How to Run the Project

1. Install Python 3.x if not already installed.
2. Clone or download this project.
3. Run the main file:
   ```bash
   python main.py
