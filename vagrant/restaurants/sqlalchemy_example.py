#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import from our database_setup file
from database_setup import Base, Restaurant, MenuItem

# The create_engine function let's our program know with which database we
# want to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the base class. This will make the connections between
# our class definitions and the corresponding tables in our database
Base.metadata.bind = engine


# Create a sessionmaker object. This stablishs a link of communication
# between our code executions and the engine we just created.
DBSession = sessionmaker(bind=engine)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# In order to create, read, delete or update information on our database,
# SQLAlchemy executes database operations via an interface called "a
# session". A session allows us to write down all the commands we want to
# execute, but not send them to the database until we call a "commit".

# Let's create a session so that we can send commands
session = DBSession()

# Lets create a restaurant
myFirstRestaurant = Restaurant(name="Pizza Palace")
# add it to the database (staging area)
session.add(myFirstRestaurant)
# and commit the change to the database
session.commit()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Optional xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Lets check if it worked. We can use our session to do queries. This will
# return a list of Restaurant objects in our database.
print session.query(Restaurant).all()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# xxxxxxxxxx Add a new menu item to a restaurant xxxxxxxxxxxxxxxxxxxxxxxxxx
cheesepizza = MenuItem(name="Cheese Pizza",
                       description=("Made with all natural igredients and"
                                    " fresh mozzarella"),
                       course="Entree",
                       price="$8.99",
                       restaurant=myFirstRestaurant);
session.add(cheesepizza)
session.commit()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Optional: Query for the menu items xxxxxxxxxxxxxxxxxxxxxxxxxxx
print
print session.query(MenuItem).all()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Optional: Query for the first menu item xxxxxxxxxxxxxxxxxxxxxx
firstResult = session.query(MenuItem).first()
print
print firstResult
# Note that we can extract column info as method names
print firstResult.name
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# xxxxxxxxxx Find Veggie Burger menu item xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# The filter_by function always return a collection of objects
veggieBurgers = session.query(MenuItem).filter_by(name="Veggie Burger")
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print '\n'

# From the loop above we saw the first one is from Urban Burger, with an id
# equal to 9. Now we can filter by id to get only that burger. Than we ask
# for "one()" to get the single value instead of a list (with one element)
UrbanVeggieBurger = session.query(MenuItem).filter_by(id=9).one()

# Update the price of the urban veggie burger
UrbanVeggieBurger.price = "$2.99"

# Add it to the database and commit
session.add(UrbanVeggieBurger)
session.commit()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# xxxxxxxxxx Delete the 'Spinach Ice Cream' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# find the ice cream item (assume there is only one item with this name
spinach = session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()
session.delete(spinach)
session.commit()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
