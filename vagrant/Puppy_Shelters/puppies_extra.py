#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from puppies import Base, Puppy, engine


#Base = declarative_base()


# Create the profile table

# Each puppy is allowed one profile which can contain a url to the puppy’s
# photo, a description about the puppy, and any special needs the puppy may
# have. Implement this table and the foreign key relationship in your code.
class PuppyProfile(Base):
    __tablename__ = "puppy_profile"
    id = Column(Integer, primary_key=True)
    url = Column(String(200))
    description = Column(String(400))
    special_needs = Column(String(150))
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    shelter = relationship(Puppy)


# The tables defined in the 'puppies.py' file were already created in the
# databse. Here we defined more tables such as PuppyProfile and therefore
# we need to call "Base.metadata.create_all" again to create the new tables
# defined here.
Base.metadata.create_all(engine)
