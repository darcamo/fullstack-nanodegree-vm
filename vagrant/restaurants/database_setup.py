#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Note que "Base" aqui é uma classe da qual nossas tabelas vão herdar.
Base = declarative_base()
# Above, the :func:`declarative_base` callable returns a new base class
# from which all mapped classes should inherit. When the class definition
# is completed, a new :class:`.Table` and :func:`.mapper` will have been
# generated.
#
# The resulting table and mapper are accessible via ``__table__`` and
# ``__mapper__`` attributes on the ``SomeClass``


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


engine = create_engine('sqlite:///restaurantmenu.db')


# The declarative_base() base class contains a MetaData object where newly
# defined Table objects are collected. This object is intended to be
# accessed directly for MetaData-specific operations. Such as, to issue
# CREATE statements for all tables:
Base.metadata.create_all(engine)
