# Dinosaur Class
class Dinosaur:
    def __init__(self, name, period, diet, image="", description=""):
        self.name = name
        self.period = period
        self.diet = diet
        self.image = image # Optional attribute for storing the image path or data
        self.description = description # Optional attribute for storing a detailed description
    
    def to_dict(self):
        return {
            'name': self.name,
            'period': self.period,
            'diet': self.diet,
            'image': self.image,
            'description': self.description
        }
    
    # Static method to create a Dinosaur object from a dictionary
    @staticmethod
    def from_dict(data):
        return Dinosaur(
            data.get('name'),
            data.get('period'),
            data.get('diet'),
            data.get('image'), # This will be None if 'image' key is not present
            data.get('description') # This will be None if 'description' key is not present
        )
    
    def __str__(self):
        return f"Nama: {self.name} | Periode: {self.period} | Diet: {self.diet}"