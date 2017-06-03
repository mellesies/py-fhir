# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import logging
import pprint

import xml.etree.ElementTree as ET
from formencode.doctest_xml_compare import xml_compare

import fhir.model
        

class TestSimpleTypes(unittest.TestCase):
    
    def test_string(self):
        t = 'test'
        s = fhir.model.string(t)
        
        self.assertTrue(isinstance(s, fhir.model.Element))
        self.assertTrue(hasattr(s, 'id'))
        self.assertTrue(hasattr(s, 'extension'))
        
        self.assertEquals(s, t)
        self.assertEquals(str(s), t)
        self.assertEquals(s+s, 2*t)
        self.assertEquals(3*s, 3*t)
        self.assertEquals(s*3, 3*t)
        
    def test_integer(self):
        t = 5
        i = fhir.model.integer(t)
        
        self.assertTrue(isinstance(i, fhir.model.Element))
        self.assertTrue(hasattr(i, 'id'))
        self.assertTrue(hasattr(i, 'extension'))
        
        self.assertEquals(i, t)
        self.assertEquals(i+i, 2*t)
        self.assertEquals(i+t, 2*t)
        self.assertEquals(t+i, 2*t)
        self.assertEquals(3*i, 3*t)

    def test_float(self):
        t = 5.0
        i = fhir.model.decimal(t)
        
        self.assertTrue(isinstance(i, fhir.model.Element))
        self.assertTrue(hasattr(i, 'id'))
        self.assertTrue(hasattr(i, 'extension'))
        
        self.assertEquals(i, t)
        self.assertEquals(i+i, 2*t)
        self.assertEquals(i+t, 2*t)
        self.assertEquals(t+i, 2*t)
        self.assertEquals(3*i, 3*t)
        self.assertEquals(i*3, 3*t)


    def test_boolean(self):
        t = fhir.model.boolean(True)
        f = fhir.model.boolean(False)
        
        self.assertTrue(isinstance(t, fhir.model.Element))
        self.assertTrue(hasattr(t, 'id'))
        self.assertTrue(hasattr(t, 'extension'))
        
        self.assertEquals(t, True)
        self.assertEquals(t and t, True)
        self.assertEquals(t or f, True)
        self.assertEquals(f, False)
    
    def test_boolean2(self):
        t = fhir.model.boolean("true")
        f = fhir.model.boolean("false")
        
        self.assertEquals(t, True)
        self.assertEquals(f, False)


    def test_dateTime(self):
        datetime_as_string = '2016-12-01T00:00:00Z'
        dt = fhir.model.dateTime(datetime_as_string)
        self.assertEquals(str(dt), datetime_as_string)
        self.assertRaises(ValueError, fhir.model.dateTime, '2016-12-01T00:00:01')
        self.assertRaises(ValueError, fhir.model.dateTime, '2016-12-01T00:01:00')
        self.assertRaises(ValueError, fhir.model.dateTime, '2016-12-01T01:00:00')
        
        
    def test_date(self):
        date_as_string = '2016-12-01'
        dt = fhir.model.date(date_as_string)
        self.assertEquals(str(dt), date_as_string)
        
    def test_time(self):
        dt = fhir.model.time('00:00:00')
        self.assertEquals(str(dt), '00:00:00')
        
