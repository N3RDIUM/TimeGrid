import json
import os

class DB:
    def __init__(self, DB_PATH: str) -> None:
        """
        This is the database handler class.
        """
        self.path = DB_PATH
        
        self.teacher_ids = os.listdir(os.path.join(self.path, 'teachers'))
        self.class_ids = os.listdir(os.path.join(self.path, 'classes'))
