# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime as dt
import logging

from . import Property
from . import FHIRBase, Element, Extension, Reference


from ._datetime import dateTime
from ._markdown import markdown
from ._string import string


__author__ = "Melle Sieswerda"
__copyright__  = "Copyright 2017, Melle Sieswerda"
__license__ = "GPL"
__version__ = "0.8"

__all__ = ['Annotation']


# ------------------------------------------------------------------------------
# Annotation
# ------------------------------------------------------------------------------
class Annotation(Element):
    """
    A  text note which also  contains information about who made the
    statement and when.
    
    Autogenerated class.
    """
    _url = 'http://hl7.org/fhir/StructureDefinition/Annotation'
    
    author = Property('author', ['Reference("http://hl7.org/fhir/StructureDefinition/Practitioner", "http://hl7.org/fhir/StructureDefinition/Patient", "http://hl7.org/fhir/StructureDefinition/RelatedPerson", "http://hl7.org/fhir/StructureDefinition/Organization")', 'string'], '0', '1')
    time = Property('time', dateTime, '0', '1')
    text = Property('text', markdown, '1', '1')
