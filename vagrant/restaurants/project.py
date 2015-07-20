#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# The route decorator binds a function to an URL
@app.route('/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurantlist.html", restaurants=restaurants)


@app.route('/restaurants/<int:restaurant_id>/')  # This URL calls HelloWorld
def restaurantMenu(restaurant_id):
    """
    """
    restaurant = session.query(Restaurant)\
                        .filter_by(id=restaurant_id)\
                        .one()
    items = session.query(MenuItem)\
                   .filter_by(restaurant_id=restaurant_id)

    # Notice that flasks looks for the templates in the 'templates' folder.
    # Also, notice how we are passing the 'restaurant' and 'items'
    # variables as keyargs. The escape code in the template will have
    # access to these variables.
    return render_template("menu.html", restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form["name"],
                           restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()

        flash("New item '{0}' created!".format(newItem.name))

        # Return the user to the main page
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:  # We got a GET request
        return render_template("newmenuitem.html", restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit/",
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem)\
                  .filter_by(restaurant_id=restaurant_id,
                             id=menu_id)\
                  .one()
    if request.method == 'POST':
        old_name = item.name
        item.name = request.form["newName"]
        session.add(item)
        session.commit()

        flash("Item '{0}' renamed to '{1}'".format(old_name, item.name))

        # Return the user to the main page
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # Render the template in 'editmenuitem.html'. The variables
        # available in the template are 'restaurant_id' and 'item'.
        return render_template("editmenuitem.html",
                               restaurant_id=restaurant_id,
                               item=item)


# Task 3: Create a route for deleteMenuItem function here
@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete/",
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem)\
                  .filter_by(restaurant_id=restaurant_id, id=menu_id)\
                  .one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()

        flash("Item '{0}' deleted".format(item.name))

        # Return the user to the main page
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # Render the template in 'deletemenuitem.html'. The variables
        # available in the template are 'restaurant_id' and 'item'.
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               item=item)


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxx Main xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
if __name__ == '__main__':
    # Thus should be a very secure password
    app.secret_key = 'super_secrete_key'

    # With debug = True the server will reload itself each time it notices
    # a code change
    app.debug = True

    # Host '0.0.0.0' tells the web server to listen on all public addresses
    app.run(host='0.0.0.0', port=5000)
