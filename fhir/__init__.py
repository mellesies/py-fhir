# -*- coding: utf-8 -*-
from __future__ import print_function
from . import model

__author__ = "Melle Sieswerda"
__copyright__  = "Copyright 2017, Melle Sieswerda"
__license__ = "GPL"
__version__ = "0.8"

DSTU2 = '1.0.2'
STU3 = '3.0.1'

serialized_examples_xml = {
    DSTU2: dict(),
    STU3: dict(),
}

serialized_examples_json = {
    DSTU2: dict(),
    STU3: dict(),
}

serialized_examples_xml[STU3]['complex_patient'] = """
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
    <deceasedBoolean value="false">
        <id value="deceasedBoolean.id"/>
    </deceasedBoolean>
</Patient>
"""

serialized_examples_xml[STU3]['patient_with_narrative'] = """
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


serialized_examples_xml[STU3]['bundle_with_patient'] = """
<Bundle xmlns="http://hl7.org/fhir">
    <id value="urn:uuid:749946d1-e6c0-4711-804b-216d6da35b85"/>
    <type value="searchset"/>
    <entry>
        <fullUrl value="http://spark.furore.com/fhir/Patient/spark47/_history/spark182"/>
        <resource>
            <Patient>
                <id value="patient2"/>
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


# XML Serialization for DSTU2 is currently equal to STU3
serialized_examples_xml[DSTU2] = serialized_examples_xml[STU3]

serialized_examples_json[STU3]['complex_patient'] = """
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
            "family": "Sieswerda",
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
    "deceasedBoolean": false,
    "_deceasedBoolean": {
        "id": "deceasedBoolean.id"
    }
}
"""
serialized_examples_json[DSTU2]['complex_patient'] = serialized_examples_json[STU3]['complex_patient'].replace('"Sieswerda"', '["Sieswerda"]')


serialized_examples_json[STU3]['bundle_with_patient'] = """
{
    "resourceType": "Bundle",
    "id": "urn:uuid:749946d1-e6c0-4711-804b-216d6da35b85",
    "type": "searchset",
    "entry": [
        {
            "fullUrl": "http://spark.furore.com/fhir/Patient/spark47/_history/spark182",
            "resource": {
                "resourceType": "Patient",
                "id": "patient2",
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
        }
    ]
}        
"""
serialized_examples_json[DSTU2]['bundle_with_patient'] = serialized_examples_json[STU3]['bundle_with_patient'].replace('"Sieswerda"', '["Sieswerda"]')

