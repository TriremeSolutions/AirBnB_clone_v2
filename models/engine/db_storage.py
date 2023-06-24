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
    def all(self, cls=None):
        """
        Query on the current databse session
        Queries all types of objects if cls is None.

        Return:
            A dictionary with k-v format:
            key: <class name>.<object id>
            value: object
        """
        dict_all = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            search = self.__session.query(cls)
            for sc in search:
                k = "{}.{}".format(type(sc).__name__, sc.id)
                dict_all[k] = sc
        else:
            cl_list = [State, City, Place, User, Amenity, Review]
            for cl in cl_list:
                search = self.__session.query(cl)
                for sc in search:
                    k = "{}.{}".format(type(sc).__name__, sc.id)
                    dict_all[k] = sc
        return (dict_all)

    def new(self, obj):
        """add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session only if:"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database.
        creates the current database session.
        """
        Base.metadata.create_all(self.__engine)
        # check imports above, ensure Base included
        this = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(this)
        self.__session = Session()

    def close(self):
        """ calls remove()"""
        self.__session.close()