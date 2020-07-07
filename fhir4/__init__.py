# -*- coding: utf-8 -*-
import os
from . import model

__author__ = "Melle Sieswerda"
__copyright__  = "Copyright 2017, Melle Sieswerda"
__license__ = "GPL"
__version__ = "0.8"

DSTU2 = '1.0.2'
STU3 = '3.0.1'
R4 = '4.0.0'


def get_example_data(name, format='xml'):
    current_dir = os.path.dirname(__file__)
    file_location = os.path.join(current_dir, f"examples/{name}.{format}")
    file_location = os.path.abspath(file_location)

    return open(file_location, 'r').read()

