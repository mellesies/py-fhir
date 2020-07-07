# -*- coding: utf-8 -*-
import os, os.path
import unittest
import logging
import pprint

import xml.etree.ElementTree as ET

from formencode.doctest_xml_compare import xml_compare
import xmldiff
import jsondiff

import json

import fhir
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

        VERSION = fhir.model.VERSION

        if VERSION <= fhir.model.FHIR_DSTU2:
            name = fhir.model.HumanName(
                use='official',
                given=['Melle', 'Sjoerd'],
                family=['Sieswerda']
            )
        elif fhir.model.FHIR_DSTU2 < VERSION <= fhir.model.FHIR_R4:
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

    def test_toJSONAttrWithoutValue(self):
        jsonstring = '{"resourceType": "Patient", "_id": {"id": "haha"}}'
        p = fhir.model.Patient()
        p.id = fhir.model.id()
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

    def test_referenceAllowedProfiles(self):
        xmlstring = fhir.get_example_data('patient-example', 'xml')
        p = fhir.model.Patient.fromXML(xmlstring)

        # _allowed_profiles

    def test_examplePatientFromXML(self):
        """Test loading and serializing a patient from/to XML."""
        xmlstring = fhir.get_example_data('patient-example', 'xml')
        p = fhir.model.Patient.fromXML(xmlstring)

        # Cannot do a direct compare due to the fact namespaces can
        # be rendered in different ways.
        self.assertEquals(p.id, 'example')
        self.assertEquals(p.identifier[0].use, 'usual')
        self.assertEquals(p.identifier[0].value, '12345')
        self.assertEquals(p.active, True)

    def test_examplePatientFromJSON(self):
        """Test loading and serializing a patient from/to JSON."""
        jsonstring = fhir.get_example_data('patient-example', 'json')

        p = fhir.model.Patient.fromJSON(jsonstring)
        diff = jsondiff.diff(jsonstring, p.toJSON(), load=True)
        self.assertEquals(diff, {})

    def test_exampleBundleFromXML(self):
        xmlstring = fhir.get_example_data('bundle-example', 'xml')
        b = fhir.model.Bundle.fromXML(xmlstring)

        # Cannot do a direct compare due to the fact namespaces can
        # be rendered in different ways.
        self.assertEquals(b.id, 'bundle-example')
        self.assertEquals(b.total, 3)
        self.assertTrue(len(b.entry), 2)
        self.assertTrue(isinstance(b.entry[0].resource, fhir.model.MedicationRequest))
        self.assertTrue(isinstance(b.entry[1].resource, fhir.model.Medication))

    def test_exampleBundleFromJSON(self):
        """Test loading and serializing a patient from/to JSON."""
        jsonstring = fhir.get_example_data('bundle-example', 'json')
        b = fhir.model.Bundle.fromJSON(jsonstring)

        diff = jsondiff.diff(jsonstring, b.toJSON(), load=True)
        self.assertEquals(diff, {})

    def test_episodeOfCareFromNative(self):
        data = {
            "resourceType": "EpisodeOfCare",
            "extension": [
                {
                    "url": "https://fhir.zakbroek.com/extensions/EpisodeOfCare-title",
                    "valueString": "Ondergewicht"
                }
            ],
            "status": "active",
            "type": [{
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/episodeofcare-type",
                        "code": "hacc",
                        "display": "Home and Community Care"
                    }
                ]
            }],
            "patient": {
            "reference": "Patient/00020"
            }
        }

        fhir.model.EpisodeOfCare.fromNative(data)

    def test_exampleQuestionnaireFromJSON(self):
        """Test loading and serializing a Questionnaire from/to JSON."""
        jsonstring = fhir.get_example_data('questionnaire-TestNesting1', 'json')
        b = fhir.model.Questionnaire.fromJSON(jsonstring)

        diff = jsondiff.diff(jsonstring, b.toJSON(), load=True)
        self.assertEquals(diff, {})

