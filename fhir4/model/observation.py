# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime as dt
import logging

from . import Property
from . import FHIRBase, Element, Extension, Reference

from .backboneelement import BackboneElement
from .domainresource import DomainResource

from ._boolean import boolean
from ._code import code
from ._datetime import dateTime
from ._instant import instant
from ._integer import integer
from ._string import string
from ._time import time

from .annotation import Annotation
from .backboneelement import BackboneElement
from .codeableconcept import CodeableConcept
from .identifier import Identifier
from .period import Period
from .quantity import Quantity
from .range import Range
from .ratio import Ratio
from .sampleddata import SampledData
from .timing import Timing

__author__ = "Melle Sieswerda"
__copyright__  = "Copyright 2017, Melle Sieswerda"
__license__ = "GPL"
__version__ = "0.8"

__all__ = ['Observation']

class ReferenceRange(BackboneElement):
    """Autogenerated class for implicit type."""
    low = Property('low', 'Quantity', '0', '1')
    high = Property('high', 'Quantity', '0', '1')
    type = Property('type', 'CodeableConcept', '0', '1')
    appliesTo = Property('appliesTo', 'CodeableConcept', '0', '*')
    age = Property('age', 'Range', '0', '1')
    text = Property('text', 'string', '0', '1')

class Component(BackboneElement):
    """Autogenerated class for implicit type."""
    code = Property('code', 'CodeableConcept', '1', '1')
    value = Property('value', ['Quantity', 'CodeableConcept', 'string', 'boolean', 'integer', 'Range', 'Ratio', 'SampledData', 'time', 'dateTime', 'Period'], '0', '1')
    dataAbsentReason = Property('dataAbsentReason', 'CodeableConcept', '0', '1')
    interpretation = Property('interpretation', 'CodeableConcept', '0', '*')
    referenceRange = Property('referenceRange', ReferenceRange, '0', '*')        


# ------------------------------------------------------------------------------
# Observation
# ------------------------------------------------------------------------------
class Observation(DomainResource):
    """
    Measurements and simple assertions made about a patient, device or
    other subject.
    
    Autogenerated class.
    """
    _url = 'http://hl7.org/fhir/StructureDefinition/Observation'
    
    identifier = Property('identifier', Identifier, '0', '*')
    basedOn = Property('basedOn', Reference("http://hl7.org/fhir/StructureDefinition/CarePlan", "http://hl7.org/fhir/StructureDefinition/DeviceRequest", "http://hl7.org/fhir/StructureDefinition/ImmunizationRecommendation", "http://hl7.org/fhir/StructureDefinition/MedicationRequest", "http://hl7.org/fhir/StructureDefinition/NutritionOrder", "http://hl7.org/fhir/StructureDefinition/ServiceRequest"), '0', '*')
    partOf = Property('partOf', Reference("http://hl7.org/fhir/StructureDefinition/MedicationAdministration", "http://hl7.org/fhir/StructureDefinition/MedicationDispense", "http://hl7.org/fhir/StructureDefinition/MedicationStatement", "http://hl7.org/fhir/StructureDefinition/Procedure", "http://hl7.org/fhir/StructureDefinition/Immunization", "http://hl7.org/fhir/StructureDefinition/ImagingStudy"), '0', '*')
    status = Property('status', code, '1', '1')
    category = Property('category', CodeableConcept, '0', '*')
    code = Property('code', CodeableConcept, '1', '1')
    subject = Property('subject', Reference("http://hl7.org/fhir/StructureDefinition/Patient", "http://hl7.org/fhir/StructureDefinition/Group", "http://hl7.org/fhir/StructureDefinition/Device", "http://hl7.org/fhir/StructureDefinition/Location"), '0', '1')
    focus = Property('focus', Reference("http://hl7.org/fhir/StructureDefinition/Resource"), '0', '*')
    encounter = Property('encounter', Reference("http://hl7.org/fhir/StructureDefinition/Encounter"), '0', '1')
    effective = Property('effective', ['dateTime', 'Period', 'Timing', 'instant'], '0', '1')
    issued = Property('issued', instant, '0', '1')
    performer = Property('performer', Reference("http://hl7.org/fhir/StructureDefinition/Practitioner", "http://hl7.org/fhir/StructureDefinition/PractitionerRole", "http://hl7.org/fhir/StructureDefinition/Organization", "http://hl7.org/fhir/StructureDefinition/CareTeam", "http://hl7.org/fhir/StructureDefinition/Patient", "http://hl7.org/fhir/StructureDefinition/RelatedPerson"), '0', '*')
    value = Property('value', ['Quantity', 'CodeableConcept', 'string', 'boolean', 'integer', 'Range', 'Ratio', 'SampledData', 'time', 'dateTime', 'Period'], '0', '1')
    dataAbsentReason = Property('dataAbsentReason', CodeableConcept, '0', '1')
    interpretation = Property('interpretation', CodeableConcept, '0', '*')
    note = Property('note', Annotation, '0', '*')
    bodySite = Property('bodySite', CodeableConcept, '0', '1')
    method = Property('method', CodeableConcept, '0', '1')
    specimen = Property('specimen', Reference("http://hl7.org/fhir/StructureDefinition/Specimen"), '0', '1')
    device = Property('device', Reference("http://hl7.org/fhir/StructureDefinition/Device", "http://hl7.org/fhir/StructureDefinition/DeviceMetric"), '0', '1')
    referenceRange = Property('referenceRange', ReferenceRange, '0', '*')
    hasMember = Property('hasMember', Reference("http://hl7.org/fhir/StructureDefinition/Observation", "http://hl7.org/fhir/StructureDefinition/QuestionnaireResponse", "http://hl7.org/fhir/StructureDefinition/MolecularSequence"), '0', '*')
    derivedFrom = Property('derivedFrom', Reference("http://hl7.org/fhir/StructureDefinition/DocumentReference", "http://hl7.org/fhir/StructureDefinition/ImagingStudy", "http://hl7.org/fhir/StructureDefinition/Media", "http://hl7.org/fhir/StructureDefinition/QuestionnaireResponse", "http://hl7.org/fhir/StructureDefinition/Observation", "http://hl7.org/fhir/StructureDefinition/MolecularSequence"), '0', '*')
    component = Property('component', Component, '0', '*')
