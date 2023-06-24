#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from uuid import uuid4
from datetime import datetime
# adapting to SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime

Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models

    Attribute:
        id (String for sqlAlchemy): BaseModel id
        created_at (DateTime for sqlAlc): time created
        updated_at (DateTime for sqlAlc): time most recently updated
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Instatntiates a new model
        
        Args:
            *args (any): not used
            **kwargs (dict): the attributes k-v pairs
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        # self.updated_at = datetime.now()
        # storage.save()
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        # remove key _sa_inst from returned dict only if it exists
        if 'sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """This, for lack of better words, deletes."""
        models.storage.delete(self)