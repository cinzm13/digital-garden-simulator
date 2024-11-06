import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

class Plant:
    def __init__(self, name, plant_type):
        self.name = name
        self.plant_type = plant_type.capitalize()
        self.stage = 0  # 0: Seed, 1: Sprout, 2: Mature
        self.last_watered = time.time()
        self.is_alive = True
        self.growth_time = self.set_growth_time()

    def set_growth_time(self):
        types = {
            'Flower': 5,
            'Tree': 15,
            'Vegetable': 10
        }
        return types.get(self.plant_type, 10)

    def water(self):
        self.last_watered = time.time()
        print(f"You watered {self.name}.")

    def grow(self):
        current_time = time.time()
        time_since_watered = current_time - self.last_watered

        if time_since_watered > self.growth_time * 2:
            self.is_alive = False
            print(f"Oh no! {self.name} has withered due to lack of water.")
        elif time_since_watered > self.growth_time:
            print(f"{self.name} needs water to continue growing.")
        elif self.stage < 2:
            self.stage += 1
            print(f"{self.name} has grown to stage {self.stage}!")
        else:
            print(f"{self.name} is fully grown.")

    def status(self):
        stages = ["Seed", "Sprout", "Mature Plant"]
        if self.is_alive:
            print(f"{self.name} ({self.plant_type}) is at stage: {stages[self.stage]}")
        else:
            print(f"{self.name} ({self.plant_type}) is no longer alive.")

class Garden:
    def __init__(self):
        self.plants = []

    def add_plant(self, plant):
        self.plants.append(plant)
        print(f"{plant.name} has been added to your garden.")

    def water_all(self):
        for plant in self.plants:
            plant.water()

    def grow_all(self):
        for plant in self.plants:
            plant.grow()

    def show_garden(self):
        for plant in self.plants:
            plant.status()

class GardenGUI:
    def __init__(self, master):
        self.master = master
        self.garden = Garden()
        self.plant_images = {}
        self.create_widgets()

    def create_widgets(self):
        # Create a canvas to display the garden
        self.canvas = tk.Canvas(self.master, width=800, height=500, bg="light blue")
        self.canvas.pack()

        # Create control buttons
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack()

        self.plant_button = tk.Button(self.control_frame, text="Plant a Seed", command=self.plant_seed)
        self.plant_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.water_button = tk.Button(self.control_frame, text="Water Plants", command=self.water_plants)
        self.water_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.grow_button = tk.Button(self.control_frame, text="Advance Time", command=self.grow_plants)
        self.grow_button.pack(side=tk.LEFT, padx=5, pady=5)

    def plant_seed(self):
        # Prompt user for plant name and type
        plant_name = simpledialog.askstring("Plant a Seed", "Enter the name of your new plant:")
        if plant_name:
            plant_type = simpledialog.askstring("Plant a Seed", "Enter the type of plant (Flower/Tree/Vegetable):")
            if plant_type:
                new_plant = Plant(plant_name, plant_type)
                self.garden.add_plant(new_plant)
                self.update_garden_display()
            else:
                messagebox.showwarning("Input Error", "Plant type cannot be empty.")
        else:
            messagebox.showwarning("Input Error", "Plant name cannot be empty.")

    def water_plants(self):
        self.garden.water_all()
        messagebox.showinfo("Water Plants", "You watered all the plants.")
        self.update_garden_display()

    def grow_plants(self):
        self.garden.grow_all()
        self.update_garden_display()

    def update_garden_display(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Display each plant in the garden
        x = 50
        y = 50
        for plant in self.garden.plants:
            if plant.is_alive:
                image = self.get_plant_image(plant)
                self.canvas.create_image(x, y, anchor=tk.NW, image=image)
                self.canvas.create_text(x + 50, y + 110, text=plant.name, font=("Arial", 12))
                x += 150
                if x > 700:
                    x = 50
                    y += 150
            else:
                # Display a gravestone or withered plant image
                self.canvas.create_text(x + 50, y + 50, text=f"{plant.name} has withered.", font=("Arial", 12))
                x += 150
                if x > 700:
                    x = 50
                    y += 150

        # Keep a reference to the images
        self.canvas.image_cache = self.plant_images.values()

    def get_plant_image(self, plant):
        # Determine the image based on the plant's stage and type
        key = (plant.plant_type.lower(), plant.stage)
        if key in self.plant_images:
            return self.plant_images[key]
        else:
            image_path = self.get_image_path(plant)
            try:
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((100, 100), Image.ANTIALIAS)
                tk_image = ImageTk.PhotoImage(pil_image)
                self.plant_images[key] = tk_image
                return tk_image
            except IOError:
                # Handle missing image files
                messagebox.showerror("Image Error", f"Image not found: {image_path}")
                return None

    def get_image_path(self, plant):
        # Map plant type and stage to image files
        base_path = "images"
        plant_type = plant.plant_type.lower()
        stage = plant.stage

        # Ensure plant_type directory exists
        if plant_type not in ["flower", "tree", "vegetable"]:
            plant_type = "flower"

        # Image filenames
        filenames = [
            f"{plant_type}_seed.png",
            f"{plant_type}_sprout.png",
            f"{plant_type}_mature.png"
        ]

        return f"{base_path}/{filenames[stage]}"

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Digital Garden Simulator")

    # Set the window size
    root.geometry("800x600")

    # Create an instance of the GardenGUI class
    app = GardenGUI(root)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
