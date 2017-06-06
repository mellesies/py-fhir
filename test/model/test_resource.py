# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import logging
import pprint
import packaging.version

import xml.etree.ElementTree as ET
from formencode.doctest_xml_compare import xml_compare

import fhir.model
from fhir.model.codeableconcept import CodeableConcept, Coding

class TestResource(unittest.TestCase):
    

    def test_observationToJSON(self):
        o = fhir.model.Observation()


    def test_compositionToJSON(self):
        c = fhir.model.Composition()


    def test_assignmentError(self):
        p = fhir.model.Patient()
        name = fhir.model.HumanName()

        with self.assertRaises(fhir.model.PropertyTypeError):
            p.active = 'this really should be a boolean'

        with self.assertRaises(fhir.model.PropertyCardinalityError):
            name.given = 'should have called append'
