#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import Base, BaseModel
# update for SQLAlch
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy import Integer, Float, String
import models
from models.amenity import Amenity
from models.review import Review


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    # for db storage
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False, overlaps="place_amenities")
    reviews = relationship("Review", backref="place", cascade="delete")

    # for fileStorage
    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Fetches linked Amenities"""
            list_amenities = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    list_amenities.append(amenity)
            return list_amenities

        @amenities.setter
        def amenities(self, value):
            """
            accepts only Amenity object for appending to
            amenity_ids list, otherwise, does nothing.
            """
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
