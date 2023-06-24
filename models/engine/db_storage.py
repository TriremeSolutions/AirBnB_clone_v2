#!/usr/bin/python3
"""SQLAlchemy DBStorage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from os import getenv


class DBStorage:
    """
    Database representation that creates the environment tables
    """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine =
        create_engine(
            "mysql+mysqldb://{}:{}@{}/{}"
            # dialect, driver
            .format(getenv("HBNB_MYSQL_USER"),
                    getenv("HBNB_MYSQL_PWD"),
                    getenv("HBNB_MYSQL_HOST"), getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
