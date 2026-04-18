# Database
import json
import os
from models.dinosaur import Dinosaur

# Database Class
class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Get the Parent Directory
        self.filepath = os.path.join(base_dir, 'data', 'dinosaurs.json')

        self.data = []
        self.load()
    
    def load(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True) # Ensure the directory exists
            with open(self.filepath, 'w') as f:
                json.dump([], f) # Create an empty list in the JSON file if it doesn't exist
            
        with open(self.filepath, 'r') as f:
            raw_data = json.load(f)
            self.data = [Dinosaur.from_dict(d) for d in raw_data]
        
    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump([d.to_dict() for d in self.data], f, indent=4)
        
    def add(self, dinosaur):
        self.data.append(dinosaur)
        self.save()
    
    def delete(self, name):
        for d in self.data:
            if d.name.lower() == name.lower():
                self.data.remove(d)
                self.save()
                return True
        return False
    
    def get_all(self):
        return self.data

    def update(self, name, new_data):
        for d in self.data:
            if d.name.lower() == name.lower():
                if new_data.get('name'):
                    d.name = new_data['name']
                if new_data.get('period'):
                    d.period = new_data['period']
                if new_data.get('diet'):
                    d.diet = new_data['diet']
                
                self.save()
                return True
        return False
    
    def search(self, keyword):
        return [
            d for d in self.data
            if keyword.lower() in d.name.lower() or
                keyword.lower() in d.period.lower() or
                keyword.lower() in d.diet.lower()
        ]