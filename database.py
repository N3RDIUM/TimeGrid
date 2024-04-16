import json
import os

class DB:
    def __init__(self, DB_PATH: str) -> None:
        """
        This is the database handler class.
        """
        self.path = DB_PATH
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
                json.dump(self.teachers[id], file)
                
        for id in self.classes.keys():
            with open(os.path.join(self.path, 'classes', id + '.json'), 'w') as file:
                json.dump(self.classes[id], file)

    def new_teacher(self, id, data):
        """
        Create a new teacher entry in the db.
        """
        self.teachers[id] = data
        print(self.teachers)
        self.sync()
        
    def update_teacher(self, id, data):
        """
        Update an existing teacher's entry in the db.
        """
        self.teachers[id].update(data)
        self.sync()
