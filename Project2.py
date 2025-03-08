import tkinter as tk
from tkinter import messagebox

# Class representing a single car
class Car:
    def __init__(self, model, price, fuel_efficiency, brand, horsepower, safety_rating, color):
        self.model = model
        self.price = price
        self.fuel_efficiency = fuel_efficiency
        self.brand = brand
        self.horsepower = horsepower
        self.safety_rating = safety_rating
        self.color = color
    
    def __repr__(self):
        return f"{self.model} ({self.brand}): ${self.price}, {self.fuel_efficiency} MPG, Safety: {self.safety_rating} Stars"

# Class representing the car shop with available cars
class CarShop:
    def __init__(self):
        self.cars = []
    
    def add_car(self, car):
        self.cars.append(car)
    
    def get_available_cars(self):
        return self.cars

# Class representing a car buyer, who can choose a car based on preferences
class CarBuyer:
    def __init__(self, budget, min_fuel_efficiency, brand_preference, min_safety_rating):
        self.budget = budget
        self.min_fuel_efficiency = min_fuel_efficiency
        self.brand_preference = brand_preference
        self.min_safety_rating = min_safety_rating
    
    def filter_cars(self, cars):
        matching_cars = [
            car for car in cars
            if car.price <= self.budget
            and car.fuel_efficiency >= self.min_fuel_efficiency
            and (self.brand_preference.lower() in car.brand.lower() or self.brand_preference == "")
            and car.safety_rating >= self.min_safety_rating
        ]
        return matching_cars

    def recommend_car(self, car_shop):
        available_cars = car_shop.get_available_cars()
        filtered_cars = self.filter_cars(available_cars)
        return filtered_cars

# GUI for the Car Recommendation System
class CarRecommendationUI:
    def __init__(self, root):
        self.car_shop = CarShop()
        self.car_shop.add_car(Car('Honda Civic', 22000, 30, 'Honda', 158, 4.5, 'Red'))
        self.car_shop.add_car(Car('Toyota Corolla', 21000, 32, 'Toyota', 139, 4.7, 'Blue'))
        self.car_shop.add_car(Car('BMW 3 Series', 35000, 25, 'BMW', 255, 4.2, 'Black'))
        self.car_shop.add_car(Car('Ford Focus', 20000, 28, 'Ford', 160, 4.3, 'White'))
        self.car_shop.add_car(Car('Chevrolet Malibu', 23000, 26, 'Chevrolet', 160, 4.4, 'Silver'))
        
        self.root = root
        self.root.title("Car Recommendation System")
        
        tk.Label(root, text="Budget (USD):").grid(row=0, column=0)
        self.budget_var = tk.StringVar()
        tk.Entry(root, textvariable=self.budget_var).grid(row=0, column=1)
        
        tk.Label(root, text="Min Fuel Efficiency (MPG):").grid(row=1, column=0)
        self.fuel_var = tk.StringVar()
        tk.Entry(root, textvariable=self.fuel_var).grid(row=1, column=1)
        
        tk.Label(root, text="Preferred Brand:").grid(row=2, column=0)
        self.brand_var = tk.StringVar()
        tk.Entry(root, textvariable=self.brand_var).grid(row=2, column=1)
        
        tk.Label(root, text="Min Safety Rating (out of 5):").grid(row=3, column=0)
        self.safety_var = tk.StringVar()
        tk.Entry(root, textvariable=self.safety_var).grid(row=3, column=1)
        
        tk.Button(root, text="Find Cars", command=self.find_cars).grid(row=4, columnspan=2)
        self.result_label = tk.Label(root, text="", justify="left")
        self.result_label.grid(row=5, columnspan=2)
        
    def find_cars(self):
        try:
            budget = float(self.budget_var.get().strip())
            min_fuel_efficiency = float(self.fuel_var.get().strip())
            brand_preference = self.brand_var.get().strip()
            min_safety_rating = float(self.safety_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for budget, fuel efficiency, and safety rating.")
            return
        
        buyer = CarBuyer(budget, min_fuel_efficiency, brand_preference, min_safety_rating)
        matching_cars = buyer.recommend_car(self.car_shop)
        
        if matching_cars:
            result_text = "Available Cars:\n" + "\n".join(
                f"{car.model} ({car.brand}): ${car.price}, {car.fuel_efficiency} MPG, Safety: {car.safety_rating} Stars"
                for car in matching_cars
            )
        else:
            result_text = "No cars available matching your preferences."
        
        self.result_label.config(text=result_text, anchor="w", justify="left")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarRecommendationUI(root)
    root.mainloop()
