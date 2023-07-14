#!/usr/bin/python3
"""
    This module defines the class FileStorage.
"""
import json
import shlex


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
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.values():
                    self.all()[key] = classes[val['__class__']](**val)
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
