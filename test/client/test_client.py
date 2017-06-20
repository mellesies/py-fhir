# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import doctest
import logging


from fhir.persistance import FHIRStore
import fhir.model
import fhir.client

from fhir.model import Bundle, Patient
from fhir.client import Client

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(fhir.client))
    return tests

class TestClient(unittest.TestCase):
    
    def setUp(self):
        pass

    # @unittest.skip('requires network connection')
    def test_get(self):
        client = Client('http://spark.furore.com/fhir/')
        id_ = 'spark47'
        
        p = client.get('Patient', id_)
        self.assertEquals(p.id, id_)
