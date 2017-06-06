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
        if fhir.model.VERSION == fhir.model.FHIR_DSTU2:
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
                        "family": ["Sieswerda"],
                        "given": [
                            "Melle",
                            "Sjoerd"
                        ]
                    }
                ]
            }
            """
        elif fhir.model.VERSION == fhir.model.FHIR_STU3:
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
                        "family": "Sieswerda",
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

    def test_marshallXMLNarrative(self):
        xmlstring = """
        <Patient xmlns="http://hl7.org/fhir">
            <id value="http://fhir.zakbroek.com/Patient/1"/>
        	<text>
        		<status value="generated"/>
        		<div xmlns="http://www.w3.org/1999/xhtml">
        			<h1>Melle Sjoerd Sieswerda</h1>
        		</div>
        	</text>
            <active value="true"/>
            <name>
                <use value="official"/>
                <family value="Sieswerda"/>
                <given value="Melle"/>
                <given value="Sjoerd"/>
            </name>
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
    
    def test_marshallXMLBundle(self):
        xmlstring = """
        <Bundle xmlns="http://hl7.org/fhir">
            <id value="urn:uuid:749946d1-e6c0-4711-804b-216d6da35b85"/>
            <type value="searchset"/>
            <entry>
                <fullUrl value="http://spark.furore.com/fhir/Patient/spark47/_history/spark182"/>
                <resource>
                    <Patient>
                        <id value="spark47"/>
                        <name>
                            <use value="official"/>
                            <family value="Sieswerda"/>
                            <given value="Melle"/>
                            <given value="Sjoerd"/>
                        </name>
                    </Patient>
                </resource>
            </entry>
        </Bundle>
        """
        b = fhir.model.Bundle.marshallXML(xmlstring)
        x1 = ET.fromstring(xmlstring)
        x2 = ET.fromstring(b.toXML())

        try:
            self.assertTrue(xml_compare(x1, x2))
        except:
            print('')
            print('*** ACTUAL ***')
            print(b.toXML())
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
        if fhir.model.VERSION == fhir.model.FHIR_DSTU2:
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
                        "family": ["Sieswerda"],
                        "given": [
                            "Melle",
                            "Sjoerd"
                        ]
                    }
                ]
            }
            """
        elif fhir.model.VERSION == fhir.model.FHIR_STU3:
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
                        "family": "Sieswerda",
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


