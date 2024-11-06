import time

def main():
    print("Welcome to the Garden Simulator!")
    plant_name = input("Enter the name of your plant: ")
    my_plant = Plant(plant_name)
    my_plant.status()
    my_plant.water()
    my_plant.grow()
    my_plant.status()

class Plant:
    def __init__(self, name):
        self.name = name
        self.stage = 0
        self.last_watered = time.time()
        self.is_alive = True
    
    def water(self):
        self.last_watered = time.time()
        print(f"You watered the {self.name}.")

    def grow(self):
        current_time = time.time()
        time_since_watered = current_time - self.last_watered

        if time_since_watered > 10:
            self.is_alive = False
            print(f"Oh no! Your {self.name} has withered due to the lack of water")
        elif self.stage < 2:
            self.stage += 1
            print(f"Your {self.name} has grown to stage {self.stage}!")
        else:
            print(f"Your {self.name} is fully grown.")
        
    def status(self):
        stages = ["Seed", "Sprout", "Mature Plant"]
        if self.is_alive:
            print(f"{self.name} is at stage: {stages[self.stage]}")
        else:
            print(f"{self.name} is no longer alive.")
    
if __name__ == "__main__":
    main()