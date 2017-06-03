# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import logging
import pprint

import xml.etree.ElementTree as ET
from formencode.doctest_xml_compare import xml_compare

import fhir.model
from fhir.model.codeableconcept import CodeableConcept, Coding

class TestResources(unittest.TestCase):
    

    def test_observationToJSON(self):
        o = fhir.model.Observation()

        # print('')
        # print('')
        # print(o.toJSON())
        # print('')

    def test_compositionToJSON(self):
        c = fhir.model.Composition()

        # print('')
        # print('')
        # print(c.toJSON())
        # print('')


    def test_assignmentErrors(self):
        p = fhir.model.Patient()
        name = fhir.model.HumanName()

        with self.assertRaises(fhir.model.PropertyTypeError):
            p.active = 'this really should be a boolean'

        with self.assertRaises(fhir.model.PropertyCardinalityError):
            name.given = 'should have called append'
