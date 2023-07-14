#!/usr/bin/python3
"""SQLAlchemy DBStorage engine"""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """
    Database representation that creates the environment tables
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
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
        if cls is None:
            state_from = self.__session.query(State).all()
            state_from.extend(self.__session.query(City).all())
            state_from.extend(self.__session.query(User).all())
            state_from.extend(self.__session.query(Place).all())
            state_from.extend(self.__session.query(Review).all())
            state_from.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            state_from = self.__session.query(cls)
        return {
                "{}.{}"
                .format(type(st).__name__, st.id): st for st in state_from
               }

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
