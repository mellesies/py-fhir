# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import logging
import pprint

import xml.etree.ElementTree as ET
from formencode.doctest_xml_compare import xml_compare
import json

import fhir.model
from fhir.model import Extension, dateTime, CodeableConcept, Coding
from fhir.model import VERSION_STR

class TestSerialization(unittest.TestCase):
    
    def getComplexPatient(self):
        p = fhir.model.Patient(id='patient1')
        p.active = True

        identifier = fhir.model.Identifier(
            value='123456789', 
            system='urn:oid:1.2.36.146.595.217.0.1'
        )
        p.identifier = [identifier]

        if fhir.model.VERSION == fhir.model.FHIR_DSTU2:
            name = fhir.model.HumanName(
                use='official', 
                given=['Melle', 'Sjoerd'], 
                family=['Sieswerda']
            )
        elif fhir.model.VERSION == fhir.model.FHIR_STU3:
            name = fhir.model.HumanName(
                use='official', 
                given=['Melle', 'Sjoerd'], 
                family='Sieswerda'
            )

        p.name = [name]
        p.gender = 'male'
        
        p.birthDate = '1980-06-09'
        extension = Extension(
            url="http://hl7.org/fhir/StructureDefinition/patient-birthTime",
            value=dateTime("1974-12-25T14:35:45-05:00")
        )
        p.birthDate.extension = [extension]
        
        p.deceased = fhir.model.boolean(False)
        p.deceased.id = 'deceasedBoolean.id'
        return p
    
    def test_toXML(self):
        xmlstring = fhir.serialized_examples_xml[VERSION_STR]['complex_patient']
        p = self.getComplexPatient()
        x1 = ET.fromstring(xmlstring)
        x2 = ET.fromstring(p.toXML())

        try:
            self.assertTrue(xml_compare(x1, x2))
        except:
            print('')
            print('*** ACTUAL ***')
            print(p.toXML())
            print('*** EXPECTED ***', end='')
            print(xmlstring)
            raise

    def test_toJSON(self):
        jsonstring = fhir.serialized_examples_json[VERSION_STR]['complex_patient']
        p = self.getComplexPatient()
        
        a, b = json.loads(jsonstring), json.loads(p.toJSON())
        a, b = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)

        try:
            self.assertEquals(a, b)
        except:
            print('')
            print('*** ACTUAL ***')
            print(p.toJSON())
            print('*** EXPECTED ***', end='')
            print(jsonstring)
            raise

    def test_toJSONAttrWithoutValue(self):
        jsonstring = '{"resourceType": "Patient", "_id": {"id": "haha"}}'
        p = fhir.model.Patient()
        p.id = None
        p.id.id = "haha"

        a, b = json.loads(jsonstring), json.loads(p.toJSON())
        a, b = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)

        try:
            self.assertEquals(a, b)
        except:
            print('')
            print('*** ACTUAL ***')
            print(p.toJSON())
            print('*** EXPECTED ***', end='')
            print(jsonstring)
            raise

    def test_fromXMLPatient(self):
        xmlstring = fhir.serialized_examples_xml[VERSION_STR]['complex_patient']
        p = fhir.model.Patient.fromXML(xmlstring)
        x1 = ET.fromstring(xmlstring)
        x2 = ET.fromstring(p.toXML())

        try:
            self.assertTrue(xml_compare(x1, x2))
        except:
            print('')
            print('*** ACTUAL ***')
            print(p.toXML())
            print('*** EXPECTED ***', end='')
            print(xmlstring)
            raise

    def test_fromXMLNarrative(self):
        xmlstring = fhir.serialized_examples_xml[VERSION_STR]['patient_with_narrative']
        p = fhir.model.Patient.fromXML(xmlstring)
        x1 = ET.fromstring(xmlstring)
        x2 = ET.fromstring(p.toXML())

        try:
            self.assertTrue(xml_compare(x1, x2))
        except:
            print('')
            print('*** ACTUAL ***')
            print(p.toXML())
            print('*** EXPECTED ***', end='')
            print(xmlstring)
            raise
    
    def test_fromXMLBundle(self):
        xmlstring = fhir.serialized_examples_xml[VERSION_STR]['bundle_with_patient']
        b = fhir.model.Bundle.fromXML(xmlstring)
        x1 = ET.fromstring(xmlstring)
        x2 = ET.fromstring(b.toXML())
        
        p = b.entry[0].resource
        self.assertTrue(isinstance(p, fhir.model.Patient))
        self.assertEquals(p.name[0].given[0], 'Melle')
        
        try:
            self.assertTrue(xml_compare(x1, x2))
        except:
            print('')
            print('*** ACTUAL ***')
            print(b.toXML())
            print('*** EXPECTED ***', end='')
            print(xmlstring)
            raise

    def test_fromJSON(self):
        jsonstring = fhir.serialized_examples_json[VERSION_STR]['complex_patient']
        p = fhir.model.Patient.fromJSON(jsonstring)                

        a, b = json.loads(jsonstring), json.loads(p.toJSON())
        a, b = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)

        try:
            self.assertEquals(a, b)
        except:
            print('')
            print('*** ACTUAL ***')
            print(p.toJSON())
            print('*** EXPECTED ***', end='')
            print(jsonstring)
            raise

    def test_fromJSONBundle(self):
        jsonstring = fhir.serialized_examples_json[VERSION_STR]['bundle_with_patient']
        bundle = fhir.model.Bundle.fromJSON(jsonstring)
        
        self.assertTrue(bundle.entry[0].resource.name[0].given[0] == "Melle")

        a, b = json.loads(jsonstring), json.loads(bundle.toJSON())
        a, b = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)

        try:
            self.assertEquals(a, b)
        except:
            print('')
            print('*** ACTUAL ***')
            print(bundle.toJSON())
            print('*** EXPECTED ***', end='')
            print(jsonstring)
            raise
        