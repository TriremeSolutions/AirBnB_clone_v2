#!/usr/bin/python3
"""
    This module defines the class FileStorage.
"""
import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    This class manages storage of hbnb models in JSON format

    Attributes:
        __file_path (str): name of the object saver json file.
        __objects (dict): dictionary storing the objects to be
        instatiated.
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        temp_dict = {}
        if cls is not None:
            prior_stored = self.__objects
            # now, retrieve the key and check whether its a class
            for k in prior_stored:
                # separate class from its id in same string
                search_cl = k.replace('.', ' ')
                # put class in its own string
                search_cl = search_cl.split()
                # check for matching values
                if (search_cl[0] == cls.__name__):
                    # create new key, its value is auto assigned
                    temp_dict[k] = self.__objects[k]
            return (temp_dict)
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """
            Saves to JSON file.
            Serializes the saved objects to the filepath
        """
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for saved in json.load(f).values():
                    name = saved["__class__"]
                    del saved["__class__"]
                    self.new(eval(name)(**saved))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes only an already existing object
        """
        if obj is not None:
            # delete the obj dict having the required key
            del self.__objects["{}.{}".format(type(obj).
                                              __name__, obj.id)]
    # 2 new methods added: get() and count()

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID
        Returns None if no object found
        """
        key = "{}.{}".format(cls.__name__, id)
        if key in self.__objects.keys():
            return self.__objects[key]
        else:
            return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage.
        """
        obj_entries = self.all(cls)
        return len(obj_entries)
