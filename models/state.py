#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
import shlex
from os import getenv


class State(BaseModel, Base):
    """
    State class, links to database table named "states"
    Inherits from Base for the MySQL database
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # define the rlationship with city table
    cities = relationship("City", backref="state", cascade="delete")

    # define the FileStorage relationship with City
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            temp = []
            # an interim placholder
            city_instances = []
            # list of all 'City' instances
            for k in models.storage.all():
                # check for City keys in the objects dict
                entry = k.replace('.', ' ')
                # parse object dict keys to separate id of key from class
                entry = entry.split()
                # break up string, placing object key in its own.
                if (entry[0] == 'City'):
                    # check if key was a City instance
                    temp.append(models.storage.all()[k])
                    # add entire k-v entry to temp list
                # now check temp list for items, if any
                for item in temp:
                    if (item.state_id == self.id):
                        # City's state_id value must match a "State" id
                        city_instances.append(item)
                return (city_instances)
