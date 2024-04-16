import json
import os

def update_nested_dict(dictionary, values):
    for key, value in values.items():
        if isinstance(value, dict):
            if key not in dictionary:
                dictionary[key] = {}
            update_nested_dict(dictionary[key], value)
        else:
            dictionary[key] = value
    return dictionary

class DB:
    def __init__(self, DB_PATH: str, PRODUCTION: bool) -> None:
        """
        This is the database handler class.
        """
        self.path = DB_PATH
        self.PRODUCTION = PRODUCTION # Could be useful later on
        self.teachers = {}
        self.classes = {}
        
        self.read()
        
    def read(self):
        """
        Read data from the db and assign it.
        """
        for id in os.listdir(os.path.join(self.path, 'teachers')):
            with open(os.path.join(self.path, 'teachers', id), 'r') as file:
                self.teachers[id.removesuffix('.json')] = json.load(file)
        
        for id in os.listdir(os.path.join(self.path, 'classes')):
            with open(os.path.join(self.path, 'classes', id), 'r') as file:
                self.classes[id.removesuffix('.json')] = json.load(file)

    def sync(self):
        """
        Write the data from memory to disk
        """
        for id in self.teachers.keys():
            with open(os.path.join(self.path, 'teachers', id + '.json'), 'w') as file:
                json.dump(self.teachers[id], file, indent=4)
                
        for id in self.classes.keys():
            with open(os.path.join(self.path, 'classes', id + '.json'), 'w') as file:
                json.dump(self.classes[id], file, indent=4)

    def new_teacher(self, id, data):
        """
        Create a new teacher entry in the db.
        """
        self.teachers[id] = data
        self.sync()
        
    def update_teacher(self, id, data):
        """
        Update an existing teacher's entry in the db.
        """
        self.teachers[id] = update_nested_dict(self.teachers[id], data)
        self.sync()
        
    def new_class(self, id, data):
        """
        Create a new class entry in the db.
        """
        self.classes[id] = data
        self.sync()
        
    def update_class(self, id, data):
        """
        Update an existing class's entry in the db.
        """
        self.classes[id] = update_nested_dict(self.classes[id], data)
        self.sync()
