#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
# update state for SQLAlchemy
from os import getenv
import models
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import Column
from models.base_model import Base
from models.city import City


class State(BaseModel, Base):
    """
    State class
    Representation for DBstorage
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    # representation for FileStorage
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Retrieves all City objects to a list"""
            # get all city values
            all_cities = models.storage.all(City).values()
            # convert to list format
            all_cities = list(all_cities)
            # create new empty list
            list_cities = []
            # iterate
            for city in all_cities:
                # check if city and state id's are a match
                if city.state_id == self.id:
                    # attach value to new list of all cities
                    list_cities.append(city)
            return list_cities
