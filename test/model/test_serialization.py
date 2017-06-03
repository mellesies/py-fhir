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

class TestSerialization(unittest.TestCase):
    
    def test_serializeXML(self):
        xmlstring = """
        <Patient xmlns="http://hl7.org/fhir">
            <id value="http://fhir.zakbroek.com/Patient/1"/>
            <identifier>
                <system value="urn:oid:1.2.36.146.595.217.0.1"/>
                <value value="123456789"/>
            </identifier>
            <active value="true"/>
            <name>
                <use value="official"/>
                <family value="Sieswerda"/>
                <given value="Melle"/>
                <given value="Sjoerd"/>
            </name>
            <gender value="male"/> 
            <deceasedBoolean value="false"/>
        </Patient>
        """
        p = fhir.model.Patient(id='http://fhir.zakbroek.com/Patient/1')
        p.active = True

        identifier = fhir.model.Identifier(
            value='123456789', 
            system='urn:oid:1.2.36.146.595.217.0.1'
        )
        p.identifier = [identifier]

        name = fhir.model.HumanName(
            use='official', 
            given=['Melle', 'Sjoerd'], 
            family=['Sieswerda']
        )
        p.name = [name]
        p.gender = 'male'
        p.deceased = fhir.model.boolean(False)

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

    def test_serializeXMLWithExtension(self):
        xmlstring = """
        <Patient xmlns="http://hl7.org/fhir">
            <id value="http://fhir.zakbroek.com/Patient/1"/>
            <birthDate value="1980-06-09">
                <extension url="http://hl7.org/fhir/StructureDefinition/patient-birthTime">
                    <valueDateTime value="1974-12-25T14:35:45-05:00"/> 
                </extension> 
            </birthDate>
        </Patient>
        """
        p = fhir.model.Patient(id='http://fhir.zakbroek.com/Patient/1')
        p.birthDate = '1980-06-09'
        extension = Extension(
            url="http://hl7.org/fhir/StructureDefinition/patient-birthTime",
            value=dateTime("1974-12-25T14:35:45-05:00")
        )
        p.birthDate.extension = [extension]

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
        

    def test_serializePatientJSON(self):
        jsonstring = """
        {
            "resourceType": "Patient",
            "id": "http://fhir.zakbroek.com/Patient/1",
            "identifier": [
                {
                    "system": "urn:oid:1.2.36.146.595.217.0.1",
                    "value": "123456789"
                }
            ],
            "active": true,
            "name": [
                {
                    "use": "official",
                    "family": [
                        "Sieswerda"
                    ],
                    "given": [
                        "Melle",
                        "Sjoerd"
                    ]
                }
            ]
        }
        """
        p = fhir.model.Patient()
        p.id = 'http://fhir.zakbroek.com/Patient/1'
        p.active = True

        identifier = fhir.model.Identifier(
            value='123456789', 
            system='urn:oid:1.2.36.146.595.217.0.1'
        )
        p.identifier.append(identifier)

        name = fhir.model.HumanName(
            use='official', 
            given=['Melle', 'Sjoerd'], 
            family=['Sieswerda']
        )
        p.name = [name]

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

    def test_serializePatientJSON2(self):
        jsonstring = """
        {
            "resourceType": "Patient",
            "_id": {
                "id": "haha"
            }
        }
        """
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


    def test_marshallXMLSimple(self):
        xmlstring = """
        <Patient xmlns="http://hl7.org/fhir">
            <id value="http://fhir.zakbroek.com/Patient/1"/>
            <identifier>
                <value value="123456789"/>
            </identifier>
            <active value="true"/>
            <name>
                <use value="official"/>
                <family value="Sieswerda"/>
                <given value="Melle"/>
                <given value="Sjoerd"/>
            </name>
            <gender value="male"/> 
            <deceasedBoolean value="true"/>
        </Patient>
        """
        p = fhir.model.Patient.marshallXML(xmlstring)
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

    def test_marshallXMLWithDate(self):
        xmlstring = """
            <Patient xmlns="http://hl7.org/fhir">
                <id value="http://fhir.zakbroek.com/Patient/1"/>
                <birthDate value="1980-06-09"/>
            </Patient>
        """
        p = fhir.model.Patient.marshallXML(xmlstring)
        x1 = ET.fromstring(xmlstring)
        x2 = ET.fromstring(p.toXML())

        self.assertTrue(xml_compare(x1, x2))

    def test_marshallXMLWithExtension(self):
        xmlstring = """
        <Patient xmlns="http://hl7.org/fhir">
            <id value="http://fhir.zakbroek.com/Patient/1"/>
            <birthDate value="1980-06-09">
                <extension url="http://hl7.org/fhir/StructureDefinition/patient-birthTime">
                    <valueDateTime value="1974-12-25T14:35:45-05:00"/> 
                </extension> 
            </birthDate>
        </Patient>
        """
        p = fhir.model.Patient.marshallXML(xmlstring)

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

    def test_marshallJSON(self):
        jsonstring = """
        {
            "resourceType": "Patient",
            "id": "http://fhir.zakbroek.com/Patient/1",
            "_id": {
                "id": "id.id"
            },
            "identifier": [
                {
                    "system": "urn:oid:1.2.36.146.595.217.0.1",
                    "value": "123456789"
                }
            ],
            "active": true,
            "name": [
                {
                    "use": "official",
                    "family": [
                        "Sieswerda"
                    ],
                    "given": [
                        "Melle",
                        "Sjoerd"
                    ]
                }
            ]
        }
        """
        p = fhir.model.Patient.marshallJSON(jsonstring)                

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


