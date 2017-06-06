# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import logging


from fhir.persistance import FHIRStore
import fhir.model
from fhir.model import *


class TestPersistance(unittest.TestCase):
    
    def setUp(self):
        self.store = FHIRStore(drop_all=True)

        self.p = Patient()
        self.p.id = 'http://fhir.zakbroek.com/Patient/1'
        self.p.active = True

        name = fhir.model.HumanName()
        name.use = 'official'
        name.given.append('Melle')
        name.given.append('Sjoerd')
        
        if fhir.model.VERSION == fhir.model.FHIR_DSTU2:
            name.family = ['Sieswerda']
        elif fhir.model.VERSION == fhir.model.FHIR_STU3:
            name.family = 'Sieswerda'
            
        self.p.name.append(name)

        self.p.deceased = fhir.model.dateTime('2016-12-01T00:00:00Z')

        identifier = fhir.model.Identifier()
        identifier.value = '123456789'
        self.p.identifier.append(identifier)

    def test_get(self):
        self.store.post(self.p)
        p = self.store.get(self.p.id)

        self.assertEquals(p.id, self.p.id)

    def test_post(self):

        self.store.post(self.p)