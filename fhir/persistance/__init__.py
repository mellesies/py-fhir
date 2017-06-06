# -*- coding: utf-8 -*-
"""Database Model declarations."""
from __future__ import unicode_literals, print_function

import datetime, time
import logging

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr

import fhir.model

__author__ = "Melle Sieswerda"
__copyright__  = "Copyright 2017, Melle Sieswerda"
__license__ = "GPL"
__version__ = "0.8"

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
object_session = Session.object_session



# ------------------------------------------------------------------------------
# Base
# ------------------------------------------------------------------------------
@as_declarative()
class Base(object):
    """Base class."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        keys = inspect(self.__class__).columns.keys()
        values = [getattr(self, key) for key in keys]
        return iter(zip(keys, values))
    # def __iter__

    @property
    def log(self):
        return logging.getLogger(self.__class__.__name__)
# class Base

class Resource(Base):
    """Example DB model class."""

    _id = Column(Integer, primary_key=True)

    # Attributes
    id = Column(String(50), index=True, unique=True)
    type = Column(String(50), index=True)
    xml = Column(Text)
# class Resource

class FHIRStore(object):
    def __init__(self, URI='sqlite:///tmp.db', drop_all=False):
        engine = create_engine(URI, convert_unicode=True)
        Session.configure(bind=engine)

        if drop_all:
            Base.metadata.drop_all(engine)

        Base.metadata.create_all(bind=engine)
    
    def get(self, id):
        """Retrieve a Resource from the database."""
        session = Session()

        persisted_resource = session.query(Resource).filter_by(id=str(id)).one()
        cls = getattr(fhir.model, persisted_resource.type)
        return cls.marshallXML(persisted_resource.xml)
    
    def post(self, resource):
        """Create a Resource in the database."""
        session = Session()

        persisted_resource = Resource(
            id=str(resource.id),
            type=resource.__class__.__name__,
            xml=resource.toXML()
        )

        session.add(persisted_resource)
        session.commit()

    def put(self, resource):
        """Update a Resource in the database."""
        pass

    def delete(self, resource):
        """Delete a Resource from the database."""
        pass
# class FHIRStore
