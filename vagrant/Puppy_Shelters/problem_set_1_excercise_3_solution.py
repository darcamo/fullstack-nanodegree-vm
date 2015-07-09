#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import datetime

# Import from our database_setup file
from puppies import Base, Shelter, Puppy
from puppies_extra import PuppyProfile, Person, Adoption

# The create_engine function let's our program know with which database we
# want to communicate with.
engine = create_engine('sqlite:///puppyshelter.db')

# # Bind the engine to the base class. This will make the connections between
# # our class definitions and the corresponding tables in our database
Base.metadata.bind = engine


# Create a sessionmaker object. This stablishs a link of communication
# between our code executions and the engine we just created.
DBSession = sessionmaker(bind=engine)

# Let's create a session so that we can send commands
session = DBSession()


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxx Exercise 3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# In this exercise you will create puppy profiles to collect even more
# information about each puppy. Each puppy is allowed one profile which can
# contain a url to the puppy’s photo, a description about the puppy, and
# any special needs the puppy may have. Implement this table and the
# foreign key relationship in your code.
description = "Cute little puppy."
special_needs = "yammy yammy food"
puppyProfile = PuppyProfile(url='/images/puppy1.jpg',
                            description=description,
                            special_needs=special_needs,
                            puppy_id=1)
session.add(puppyProfile)
session.commit()
