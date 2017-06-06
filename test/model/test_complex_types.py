# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import logging
import pprint

import xml.etree.ElementTree as ET
from formencode.doctest_xml_compare import xml_compare

import fhir.model
        

class TestComplexTypes(unittest.TestCase):
    
    def test_humanname(self):
        name = fhir.model.HumanName()
        name.use = 'official'
        name.given.append('Melle')
        name.given.append('Sjoerd')
        
        if fhir.model.VERSION == fhir.model.FHIR_DSTU2:
            name.family = ['Sieswerda']
        elif fhir.model.VERSION == fhir.model.FHIR_STU3:
            name.family = 'Sieswerda'

        # print(name.toXML())
        
    def test_extension(self):
        xmlstring = """
        <Extension url="http://example.com/ExtensionThingy">
            <valueString value="Hurray for me"/>
        </Extension>
        """

        ext = fhir.model.Extension()
        ext.url = 'http://example.com/ExtensionThingy'
        ext.value = fhir.model.string('Hurray for me')

        x1 = ET.fromstring(xmlstring)
        x2 = ET.fromstring(ext.toXML())
        self.assertTrue(xml_compare(x1, x2))

        
