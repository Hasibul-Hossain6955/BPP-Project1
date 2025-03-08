import tkinter as tk
from tkinter import messagebox

class Room:
    def __init__(self, room_number, room_type, price, amenities):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.amenities = amenities  # List of amenities (e.g., Wi-Fi, air conditioning)
    
    def __repr__(self):
        return f"Room {self.room_number}: {self.room_type}, Price: ${self.price}, Amenities: {', '.join(self.amenities)}"

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []  # List to store available rooms

    def add_room(self, room):
        self.rooms.append(room)

    def get_available_rooms(self):
        return self.rooms

class Customer:
    def __init__(self, budget, preferred_room_type, required_amenities):
        self.budget = budget
        self.preferred_room_type = preferred_room_type
        self.required_amenities = required_amenities

    def filter_rooms(self, rooms):
        matching_rooms = [
            room for room in rooms
            if room.price <= self.budget
            and (self.preferred_room_type.lower() in room.room_type.lower() or self.preferred_room_type == "")
            and all(amenity in room.amenities for amenity in self.required_amenities)
        ]
        return matching_rooms

    def offer_room(self, hotel):
        available_rooms = hotel.get_available_rooms()
        filtered_rooms = self.filter_rooms(available_rooms)
        return filtered_rooms

class HotelBookingUI:
    def __init__(self, root):
        self.hotel = Hotel("Grand Hotel")
        self.hotel.add_room(Room(101, "Single", 50, ["WiFi", "TV"]))
        self.hotel.add_room(Room(102, "Double", 80, ["WiFi", "AC", "TV"]))
        self.hotel.add_room(Room(103, "Suite", 150, ["WiFi", "AC", "TV", "Mini Bar"]))
        self.hotel.add_room(Room(104, "Single", 55, ["WiFi", "TV", "Balcony"]))
        self.hotel.add_room(Room(105, "Double", 90, ["WiFi", "AC", "TV", "Balcony"]))

        self.root = root
        self.root.title("Hotel Room Booking Assistant")

        tk.Label(root, text="Budget:").grid(row=0, column=0)
        self.budget_var = tk.StringVar()
        tk.Entry(root, textvariable=self.budget_var).grid(row=0, column=1)

        tk.Label(root, text="Preferred Room Type:").grid(row=1, column=0)
        self.room_type_var = tk.StringVar()
        tk.Entry(root, textvariable=self.room_type_var).grid(row=1, column=1)

        tk.Label(root, text="Amenities (comma-separated):").grid(row=2, column=0)
        self.amenities_var = tk.StringVar()
        tk.Entry(root, textvariable=self.amenities_var).grid(row=2, column=1)

        tk.Button(root, text="Find Rooms", command=self.find_rooms).grid(row=3, columnspan=2)
        self.result_label = tk.Label(root, text="", justify="left")
        self.result_label.grid(row=4, columnspan=2)

    def find_rooms(self):
        try:
            budget = int(self.budget_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget.")
            return

        room_type = self.room_type_var.get().strip()
        amenities = [a.strip() for a in self.amenities_var.get().split(",") if a.strip()]

        customer = Customer(budget, room_type, amenities)
        matching_rooms = customer.offer_room(self.hotel)

        if matching_rooms:
            result_text = "Available Rooms:\n" + "\n".join(
                f"Room {room.room_number}: {room.room_type}, Price: ${room.price}, Amenities: {', '.join(room.amenities)}"
                for room in matching_rooms
            )
        else:
            result_text = "No rooms available matching your preferences."
        
        self.result_label.config(text=result_text, anchor="w", justify="left")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingUI(root)
    root.mainloop()
