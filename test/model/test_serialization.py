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

complex_patient_xml = """
<Patient xmlns="http://hl7.org/fhir">
    <id value="patient1"/>
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
    <birthDate value="1980-06-09">
        <extension url="http://hl7.org/fhir/StructureDefinition/patient-birthTime">
            <valueDateTime value="1974-12-25T14:35:45-05:00"/> 
        </extension> 
    </birthDate>
    <deceasedBoolean value="false"/>
</Patient>
"""

# This structure is based on DSTU2
complex_patient_json_dict = json.loads("""
{
    "resourceType": "Patient",
    "id": "patient1",
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
    ],
    "gender": "male",
    "birthDate": "1980-06-09",
    "_birthDate": {
        "extension": [
            {
                "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                "valueDateTime": "1974-12-25T14:35:45-05:00"
            }
        ]
    },
    "deceasedBoolean": false
}
""")

if fhir.model.VERSION == fhir.model.FHIR_STU3:
    # STU3 changes the cardinality of 'name' to [0..1]
    complex_patient_json_dict['name'][0]['family'] = 'Sieswerda'
    
complex_patient_json = json.dumps(complex_patient_json_dict)



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
        return p
    
    def test_toXML(self):
        p = self.getComplexPatient()
        x1 = ET.fromstring(complex_patient_xml)
        x2 = ET.fromstring(p.toXML())

        try:
            self.assertTrue(xml_compare(x1, x2))
        except:
            print('')
            print('*** ACTUAL ***')
            print(p.toXML())
            print('*** EXPECTED ***', end='')
            print(complex_patient_xml)
            raise

    def test_toJSON(self):
        p = self.getComplexPatient()
        
        a, b = json.loads(complex_patient_json), json.loads(p.toJSON())
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

    def test_fromXMLPatient(self):
        p = fhir.model.Patient.fromXML(complex_patient_xml)
        x1 = ET.fromstring(complex_patient_xml)
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
        xmlstring = """
        <Patient xmlns="http://hl7.org/fhir">
            <id value="patient1"/>
        	<text>
        		<status value="generated"/>
        		<div xmlns="http://www.w3.org/1999/xhtml">
        			<h1>Melle Sjoerd Sieswerda</h1>
        		</div>
        	</text>
        </Patient>
        """
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
        if fhir.model.VERSION == fhir.model.FHIR_DSTU2:
            jsonstring = """
            {
                "resourceType": "Patient",
                "id": "patient1",
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
                "id": "patient1",
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


