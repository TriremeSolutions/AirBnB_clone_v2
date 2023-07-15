#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel
# update Review sql
from models.base_model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy import Column


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
