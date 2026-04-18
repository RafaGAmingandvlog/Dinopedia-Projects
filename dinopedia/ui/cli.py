# User Interface for Dinopedia CLI
from models.dinosaur import Dinosaur

# Class CLI
class CLI:
    def __init__(self, db):
        self.db = db

    def run(self):
        while True:
            print("🦖 DINOPEDIA (CLI) 🦕")
            print("1. Add Dinosaur"
                  "\n2. Delete Dinosaur"
                  "\n3. View Dinosaurs"
                  "\n4. Edit Dinosaur"
                  "\n5. Search Dinosaur"
                  "\n6. Exit")
            choice = input("Choose an option(1-6): ")

            if choice == '1':
                self.add_dinosaur()
            elif choice == '2':
                self.delete_dinosaur()
            elif choice == '3':
                self.view_dinosaurs()
            elif choice == '4':
                self.edit_dinosaur()
            elif choice == '5':
                self.search_dinosaur()
            elif choice == '6':
                print("Thank you for using Dinopedia!")
                break
            else:
                print("Invalid option. Please choose between 1-6.")
            
    def add_dinosaur(self):
        print("== 🦖 Add Dinosaur 🦕 ==")
        name = input("Enter dinosaur name: ")
        period = input("Enter dinosaur period: ")
        diet = input("Enter dinosaur diet: ")

        dino = Dinosaur(name, period, diet)
        self.db.add(dino)
        print(f"Dinosaur '{name}' added successfully!")
        
    def delete_dinosaur(self):
        print("== 🦖 Delete Dinosaur 🦕 ==")
        name = input("Enter the name of the dinosaur to delete: ")
        if self.db.delete(name):
                print(f"Dinosaur '{name}' deleted successfully!")
        else:
            print(f"Dinosaur '{name}' not found.")
        
    def view_dinosaurs(self):
        print("== 🦖 View Dinosaurs 🦕 ==")
        dinosaurs = self.db.get_all()
        if not dinosaurs:
            print("No dinosaurs found.")
        else:
            for d in dinosaurs:
                print(d)
        
    def edit_dinosaur(self):
        print("== 🦖 Edit Dinosaur 🦕 ==")
        name = input("Enter the name of the dinosaur to edit: ")
        dinosaurs = self.db.get_all()
        for d in dinosaurs:
            if d.name.lower() == name.lower():
                new_name = input("New name (press Enter to keep unchanged): ")
                new_period = input("New period (press Enter to keep unchanged): ")
                new_diet = input("New diet (press Enter to keep unchanged): ")

                new_data = {}
                if new_name:
                    new_data['name'] = new_name
                if new_period:
                    new_data['period'] = new_period
                if new_diet:
                    new_data['diet'] = new_diet

                if self.db.update(name, new_data):
                    print(f"Dinosaur '{name}' updated successfully!")
                else:
                    print(f"Failed to update dinosaur '{name}'.")
                    return
            
        print(f"Dinosaur '{name}' not found.")
        
    def search_dinosaur(self):
        print("== 🦖 Search Dinosaur 🦕 ==")
        keyword = input("Enter keyword to search: ")
        results = self.db.search(keyword)
        if not results:
            print("No dinosaurs found matching the keyword.")
        else:
            for d in results:
                print(d)
        