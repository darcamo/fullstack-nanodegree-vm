#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import datetime

# Import from our database_setup file
from puppies import Base, Shelter, Puppy

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
# xxxxxxxxxxxxxxx Exercise 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# 1. Query all of the puppies and return the results in ascending
# alphabetical order
print "    All puppies ordered by name"
q = session.query(Puppy)
q_ordered_alpha = q.order_by(Puppy.name)
for v in q_ordered_alpha.all():
    print "{0}\t{1}\tWeight: {2}\tShelter: {3}".format(
        v.name.ljust(8), v.dateOfBirth, round(v.weight, 2), v.shelter.name)
print "\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# 2. Query all of the puppies that are less than 6 months old organized by
# the youngest first
print "    Puppied with less than 6 months ordered by birthdate"
six_months = datetime.timedelta(days=6*30)
now = datetime.datetime.now()
q_young_ordered_how_old = q.filter(Puppy.dateOfBirth > (now - six_months)).order_by(Puppy.dateOfBirth)
for v in q_young_ordered_how_old.all():
    print "{0}\t{1}\tWeight: {2}\tShelter: {3}".format(
        v.name.ljust(8), v.dateOfBirth, round(v.weight, 2), v.shelter.name)
print "\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# Query all puppies by ascending weight
print "    All puppies ordered by weight"
q_weight_ordered = q.order_by(Puppy.weight)
for v in q_weight_ordered.all():
    print "{0}\t{1}\tWeight: {2}\tShelter: {3}".format(
        v.name.ljust(8), v.dateOfBirth, round(v.weight, 2), v.shelter.name)
print "\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# Query all puppies grouped by the shelter in which they are staying
print "    All puppies grouped by shelter"
q_group_shelter = q.order_by(Puppy.shelter_id).order_by(Puppy.name)
for v in q_group_shelter.all():
    print "{0}\t{1}\tWeight: {2}\tShelter: {3}".format(
        v.name.ljust(8), v.dateOfBirth, round(v.weight, 2), v.shelter.name)
print "\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# Print how many puppied there are in each shelter. Note that we would need
# to do a join with the shelter table to be able to get the shelter names
print session.query(func.count(Puppy.shelter_id)).group_by(Puppy.shelter_id).all()
