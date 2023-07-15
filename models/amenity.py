#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
# update amenity SQLAlch
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """the Amenities linked to Places"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)
