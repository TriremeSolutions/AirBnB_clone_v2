#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel
# update Review sql
from models.base_model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Column


class Review(BaseModel):
    """ Review classto store review information """
    place_id = ""
    user_id = ""
    text = ""
