# -*- coding: utf-8 -*-
"""FHIR Resources & Elements in Python."""
import sys
import inspect
import packaging.version
from collections import OrderedDict
from datetime import datetime
import dateutil.parser
import inspect
import re
import logging
import pprint
import html

import xml.etree.ElementTree as ET
import xml.dom.minidom
import json

__author__ = "Melle Sieswerda"
__copyright__  = "Copyright 2017, Melle Sieswerda"
__license__ = "GPL"
__version__ = "0.8"

__all__ = [
    'inf',
    'PropertyCardinalityError',
    'PropertyTypeError',
    'PropertyDefinition',
    'Property',
    'PropertyList',
    'markdown',
    'integer',
    'dateTime',
    'unsignedInt',
    'code',
    'date',
    'decimal',
    'uri',
    'canonical',
    'url',
    'id',
    'base64Binary',
    'time',
    'oid',
    'positiveInt',
    'string',
    'boolean',
    'uuid',
    'instant',
    'xhtml',
    'Address',
    'Annotation',
    'Attachment',
    'BackboneElement',
    'Bundle',
    'CodeableConcept',
    'Coding',
    'Composition',
    'ContactDetail',
    'ContactPoint',
    'DomainResource',
    'Dosage',
    'Duration',
    'Element',
    'Extension',
    'FHIRBase',
    'HumanName',
    'Identifier',
    'Medication',
    'MedicationRequest',
    'Meta',
    'Narrative',
    'Observation',
    'Patient',
    'Period',
    'Quantity',
    'Questionnaire',
    'QuestionnaireResponse',
    'Range',
    'Ratio',
    'Reference',
    'Reference',
    'SampledData',
    'Signature',
    'Timing',
    'UsageContext',
]

# Module global
FHIR_STU3 = packaging.version.parse('3.0.1')
FHIR_DSTU2 = packaging.version.parse('1.0.2')
FHIR_R4 = packaging.version.parse('4.0.0')
VERSION = packaging.version.parse('4.0.0')
VERSION_STR = '4.0.0'

SUPPORTED_FORMATS = ['xml', 'json']

inf = float('inf')

PRIMITIVE_TYPES = OrderedDict([
    # ('Element', 'Element'),
    ('markdown', 'str'),
    ('integer', 'int'),
    ('dateTime', 'dateTimeBase'),
    ('unsignedInt', 'int'),
    ('code', 'str'),
    ('date', 'dateTimeBase'),
    ('decimal', 'float'),
    ('uri', 'str'),
    ('id', 'str'),
    ('base64Binary', 'str'),
    ('time', 'dateTimeBase'),
    ('oid', 'str'),
    ('positiveInt', 'int'),
    ('string', 'str'),
    ('boolean', 'bool'),
    ('uuid', 'str'),
    ('instant', 'dateTimeBase'),
    ('xhtml', 'str'),
])

def stars(newline_before=False, n=80):
    if newline_before:
        print()
    print('*' * n)

def upper_first_letter(attr):
    return attr[0].upper() + attr[1:]

def lower_first_letter(attr):
    return attr[0].lower() + attr[1:]

def split_namespace(element_or_tag):
    if isinstance(element_or_tag, ET.Element):
        tag = element_or_tag.tag
    else:
        tag = element_or_tag
    
    m = re.match('\{(.*)\}', tag)
    ns_with_accolades = m.group(0) if m else ''
    ns_without_accolades = m.group(1) if m else ''
    return ns_without_accolades, tag.replace(ns_with_accolades, '')

def eval_type_string(type_, module=None):
    """Evaluate PropertyDefinition.type."""
    if isinstance(type_, str):
        # Lazily evaluated type
        if module:
            try:
                attr = getattr(module, type_)
            except AttributeError:
                pass
            else:
                return attr

        try:
            # This will work for strings that contain a class type
            attr = getattr(sys.modules[__name__], type_)
        except AttributeError:
            # It could be that the string actually evaluates to an instance, 
            # for example:
            # Reference(["http://hl7.org/fhir/StructureDefinition/Organization"])
            stars(True)
            print('type_: ', type)
            attr = eval(type_)
            print('attr: ', attr)
            stars()

        return attr

    elif isinstance(type_, list):
        return [eval(t) if (type(t) == str) else t for t in type_]        

    else:
        return type_


# ------------------------------------------------------------------------------
# Exceptions & Errors
# ------------------------------------------------------------------------------
class PropertyCardinalityError(Exception):
    def __init__(self, method, description):
        if description.cmax == 1:
            message = "Cannot {} a list as value for property '{}': cardinality [{}..{}]"
        else:
            message = "Cannot {} property '{}': cardinality [{}..{}]"
            
        message = message.format(method, description.name, description.cmin, description.cmax)
        super(PropertyCardinalityError, self).__init__(message)
# class PropertyCardinalityError

class PropertyTypeError(Exception):
    def __init__(self, type_, description):
        msg = "Expected '{}' but got '{}' for '{}'".format(description.type, type_, description.name)
        super(PropertyTypeError, self).__init__(msg)
# class PropertyTypeError

class InvalidAttributeError(Exception):
    def __init__(self, resource_or_element, attr):
        msg = "The attribute '{}' is not a valid property for '{}'.".format(attr, resource_or_element)
        super(InvalidAttributeError, self).__init__(msg)
# class InvalidAttributeError

class UnsupportedFormatError(Exception):
    def __init__(self, format_):
        message = "The format '{}' is not (yet) supported!".format(format_)
        super(UnsupportedFormatError, self).__init__(message)
# class UnsupportedFormatError

# ------------------------------------------------------------------------------
# Property classes to declaratively define FHIR model.
# ------------------------------------------------------------------------------
class PropertyDefinition(object):
    """Definition of an attribute of a Resource or Element."""
    def __init__(self, name, type_, cmin, cmax, repr_='element'):
        assert name.find(' ') < 0, "'name' should not contain spaces."
        
        cmin = int(cmin)
        if cmax == '*':
            cmax = inf
        else:
            cmax = int(cmax)
        
        self.name = name
        self.type = type_
        self.cmin = cmin
        self.cmax = cmax
        self.repr = repr_
    
    def __repr__(self):
        params = {
            'name': self.name,
            'type': self.type,
            'cmin': self.cmin,
            'cmax': self.cmax,
            'repr': self.repr,
        }
        return "PropertyDefinition('{name}', '{type}', '{cmin}', '{cmax}', '{repr}')".format(**params)
# class PropertyDefinition

class PropertyMixin(object):
    """
        Provides methods to coerce (~cast) native types (str, int) to FHIR types 
        (string, decimal). Used by Property and PropertyList.
    """
    def coerce_type(self, value):
        """Coerce (~cast) value to correspond to PropertyDefinition."""
        logger = logging.getLogger('PropertyMixin')

        if value is None:
            return None

        # self.definition: PropertyDefinition
        # `type_` can be:
        # - a string (lazily evaluated type)
        # - a class
        # - a list
        # - an instance other than a list (e.g. a type with parameters)
        type_ = self.definition.type
        
        # PropertyDefinition.type might defined as string --> lazily evaluate.
        # if isinstance(type_, str):
        #     type_ = eval_type_string(type_)
        try:
            module = None
            if isinstance(value, Element):
                module = inspect.getmodule(value)

            type_ = eval_type_string(type_, module)
        except:
            print()
            print('this is not supposed to happen')
            print('type_: ', type_, type(type_))
            print('value: ', value, type(value))
            raise


        # At this point, self.definition.type can be:
        # - a class
        # - a list
        # - an instance other than a list (a type with parameters)

        # Check for multi typed properties first. isinstance will complain if
        # it receives a list of strings as 2nd argument.
        if isinstance(type_, list):
            return self.coerce_multi_type(value, type_)

        # If value already has the correct type, we don't need to do anything.
        if inspect.isclass(type_) and isinstance(value, type_):
            return value

        # If we're still here, try to coerce/cast.
        # This has a side effect: any current value will be replaced by a new instance!
        try:
            # print('casting value {} to {}'.format(value, type_))
            if isinstance(type_, Reference):
                stars(True)
                print('type_, value: ', type_, value)
                stars()

            return type_(value)
        except Exception as e:
            raise PropertyTypeError(value.__class__.__name__, self.definition)
    # def coerce_type    
    
    def coerce_multi_type(self, value, types):
        """
            Coerce 'value' to a type in 'types'.

            For properties that support more than one type, first check if the
            provided value actually is of one of these types. If not, try to cast
            to a supported value by simply trying each supported type.
            
            Example of a property that supports more than one type:
                multi = Property(PropertyDefinition('multi', ['boolean', 'dateTime'], '0', '1'))
        """
        if isinstance(value, Element):
            if isinstance(value, Reference):
                for t in types:
                    if not inspect.isclass(t) and isinstance(t, Reference):
                        return value

                raise PropertyTypeError(type(value).__name__, self.definition)

            elif type(value) not in types:
                raise PropertyTypeError(type(value).__name__, self.definition)
        
            return value
        
        # Ok, so value is not (yet) a fhir type. Try to find a supported type.
        for type_ in self.definition.type:
            constructor = getattr(sys.modules[__name__], type_)

            try:
                value = constructor(value)
            except PropertyTypeError as e:
                # print("Apparently '{}' is not a '{}'".format(value, type_))
                pass
            else:
                return value
        
        # FIXME: change to more meaningful exception!
        raise Exception("Could not find a proper type for value '{}' in {}".format(value, self.definition.type))
    # def coerce_multi_type
# class PropertyMixin
        
class Property(PropertyMixin):
    """Property of a Resource or Element.

        This class defines logic to ensure that Resource/Element (and 
        subclasses) behave much like regular Python objects, while providing
        functionality specific to the FHIR standard.
    """
    _cls_counter = 0
    
    @classmethod
    def __get_creation_counter(cls):
        cls._cls_counter += 1
        return cls._cls_counter
    
    def __init__(self, name, type_, cmin, cmax, repr_='element'):
        """Create new Property instance."""
        self._creation_order = self.__get_creation_counter()
        self.definition = PropertyDefinition(name, type_, cmin, cmax, repr_)
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            # instance attribute accessed on class, return self
            return self
        
        # instance attribute accessed on instance, return value
        if (self.definition.cmax > 1):
            instance._property_values.setdefault(self.name, PropertyList(self.definition))
        
        return instance._property_values.get(self.name)
    
    def __set__(self, instance, value):
        if self.definition.cmax > 1: 
            if isinstance(value, list):
                # Create the list if necessary
                instance._property_values.setdefault(self.name, PropertyList(self.definition))

                # Clear the list
                del instance._property_values[self.name][:]

                # Populate the list with the new values
                for item in value:
                    instance._property_values[self.name].append(item)
            
            else:
                raise PropertyCardinalityError('set', self.definition)
        
        else:
            if isinstance(value, list):
                raise PropertyCardinalityError('set', self.definition)
            
            elif isinstance(self.definition.type, Reference):
                instance._property_values[self.name] = value

            else:
                instance._property_values[self.name] = self.coerce_type(value)

    def __repr__(self):
        d = self.definition
        s = f"Property('{d.name}', {d.type}, {d.cmin}, {d.cmax}, '{d.repr}')"
        return s
    
    
    def __lt__(self, other):
        return True
# class Property

class DateTimeProperty(Property):
    def __set__(self, instance, value):
        if value is not None:
            instance._checkRegEx(value)

        super().__set__(instance, value)
# class DateTimeProperty

class PropertyList(list, PropertyMixin):
    """PropertyList is used by Property when cardinality > 1."""
    
    def __init__(self, definition, *args, **kwargs):
        """Create a new PropertyList instance.
        Note that minimum cardinality is not enforced when calling 'append'.
         
        :param PropertyDefinition definition: Description of the property.
        """
        super(PropertyList, self).__init__(*args, **kwargs)
        self.definition = definition

    def insert(self, i, x):
        """Insert a value into the list at position i."""
        # This raises a PropertyTypeError if x has an incorrect value.
        x = self.coerce_type(x)
        
        if len(self) >= self.definition.cmax:
            raise PropertyCardinalityError('insert', self.definition)
            
        super(PropertyList, self).insert(i, x)
         
    def append(self, x):
        """Append a value to the list."""
        # This raises a PropertyTypeError if x has an incorrect value.
        x = self.coerce_type(x)
        
        if len(self) >= self.definition.cmax:
            raise PropertyCardinalityError('append', self.definition)
            
        super(PropertyList, self).append(x)
    
    def toNative(self):
        return [i.toNative() for i in self]
# class PropertyList   


# ------------------------------------------------------------------------------
# Base classes
# ------------------------------------------------------------------------------
class FHIRBase(object):
    """Base class for all FHIR resources and elements."""
    _allowed_attributes = ['_property_values']

    def __init__(self, **kwargs):
        """Create a new instance."""
        self.__dict__['_property_values'] = dict()
        self.__dict__['log'] = logging.getLogger(self.__class__.__name__)
        
        self._set(**kwargs)
    # def __init__
    
    def __setattr__(self, attr, value):
        """x.attr = value <==> setattr(x, attr, value)

            Additionally, raises an InvalidAttributeError when trying to assign a 
            value to an attribute that is not part of the Resource/Element definition.
        """
        if (attr not in self._allowed_attributes) \
            and (attr not in self._getProperties()) \
            and (not attr.startswith('_')):
            raise InvalidAttributeError(type(self).__name__, attr)

        super().__setattr__(attr, value)
    # def __setattr__

    def _set(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    @classmethod
    def _getProperties(cls):
        """Return a list of attribute names that are of type 'Property'. 
        
            The list is sorted by order of definition.
        """
        properties = []
        for attr in dir(cls):
            a = getattr(cls, attr)
            if isinstance(a, Property):
                properties.append(a)
                
        properties.sort(key=lambda i: i._creation_order)
        properties = [p.definition.name for p in properties]
        
        return properties
    # def _getProperties

    @classmethod
    def _getPropertyDetailsForName(cls, name):
        """Return Property and (expected) type for attribute with 'name'."""
        name = name.replace('_', '')
        
        if not hasattr(cls, name):
            # We might be dealing with a value[x] property!
            for attr in cls._getProperties():
                if name.startswith(attr):
                    type_ = name.replace(attr, '')

                    if type_.startswith('Reference'):
                        # Get the Property
                        property_ = getattr(cls, attr)

                    else:
                        # FIXME: make sure this works for things like CodeableConcepts too ...
                        # valueBoolean --> boolean
                        type_ = lower_first_letter(type_)
                    
                    # valueBoolean --> value
                    name = attr
                    break
            else:
                # If no break occurred.
                msg = "Cannot find property '{}' on resource '{}'"
                raise Exception(msg.format(name, cls.__name__))
        else:
            type_ = ''
        
        # Get the Property
        property_ = getattr(cls, name)

        # If type_ was not explicitly defined by the tag name, get it from the
        # definition.
        if not type_:
            type_ = property_.definition.type
        
        # definition.type may be a string to facilitate lazy evaluation.
        try:
            type_ = eval_type_string(type_, inspect.getmodule(cls))
        except:
            stars(True)
            print('Could not evaluate type ...')
            print('type_:', type_)
            print('cls: ', cls, type(cls))
            print('cls.__module__: ', cls.__module__)
            print(inspect.getmodule(cls))
            stars()
            raise

        return property_, property_.definition, type_
    # def _getPropertyDetailsForName
    
    @classmethod
    def getType(cls):
        return cls.__name__
    
    @classmethod
    def loads(self, string, format_='xml'):
        if format_ in SUPPORTED_FORMATS:
            format_ = format_.upper()
            func = getattr(self, 'from' + format_)
            return func(string)
        
        raise UnsupportedFormatError(format_)
    # def loads
    
    @classmethod
    def fromXML(cls, xmlstring):
        """Marshall a Resource from its XML representation."""
        log = logging.getLogger(cls.__name__)
        # Remove the default namespace definition, makes life a bit easier
        # when using ElementTree.
        xmlstring = re.sub('\\sxmlns="[^"]+"', '', xmlstring, count=1)
        
        # Parse the string using ElementTree
        root = ET.fromstring(xmlstring)
        
        # Sanity check
        if root.tag != cls.__name__:
            # log.warn('*** WARNING: trying to marshall a {} in a {} ***'.format(root.tag, cls.__name__))
            class_ = eval_type_string(root.tag)
            
            if not issubclass(class_, cls):
                raise Exception('Cannot marshall a {} from a {}: not a subclass!'.format(root.tag, cls.__name__))
            
            return class_()._fromXML(root)
        
        return cls()._fromXML(root)
    # def fromXML_
    
    def _fromXML(self, xml):
        # Iterate over *my* properties.
        for tag in xml:
            ns, tag_name = split_namespace(tag)
            prop, prop_def, prop_type = self._getPropertyDetailsForName(tag_name)
            
            # If the namespace is xhtml, we shouldn't parse the tree any 
            # further and just try to assign the xhtml to the property.
            if ns == 'http://www.w3.org/1999/xhtml':
                value = ET.tostring(tag, 'unicode')
                value = value.replace('html:', '')
                value = value.replace(':html', '')
            
            # Inline resources are handled a little differently
            elif inspect.isclass(prop_type) and issubclass(prop_type, Resource):
                children = list(tag)
                resource_element = children[0]
                resource_type = eval_type_string(resource_element.tag)
                value = resource_type()
                value._fromXML(resource_element)
            
            # Then it must be a simple or complex type
            else:
                value = prop_type(**tag.attrib)
                value._fromXML(tag)

            if prop_def.cmax == 1:
                setattr(self, prop.name, value)
            elif prop_def.cmax > 1:
                getattr(self, prop.name).append(value)

        return self
    # def _fromXML

    @classmethod
    def fromJSON(cls, jsonstring):
        """Marshall a Resource from its JSON representation."""
        jsondict = json.loads(jsonstring)
        resourceType = jsondict.pop('resourceType')

        if resourceType != cls.__name__:
            class_ = eval_type_string(resourceType)
            
            if not issubclass(class_, cls):
                raise Exception('Cannot marshall a {} from a {}: not a subclass!'.format(root.tag, cls.__name__))
            
            return class_()._fromJSON(jsondict)
            
        return cls()._fromJSON(jsondict)
    # def fromJSON

    def _fromJSON(self, obj):
        if isinstance(obj, dict):
            # Complex type defining *my* attributes
            return self._fromDict(obj)

        if isinstance(obj, list):
            # List with values for self.attr_name
            return 
        
        # Simple type!
        return obj

    def _fromDict(self, jsondict):
        # Iterate over *my* attributes
        processed = []
        
        # First the keys starting with an underscore ('_')
        # These items contain the extended information for simple
        # types: {'id': 'patient1', '_id': {'id': 'id.id'}}
        for attr, obj in jsondict.items():
            if not attr.startswith('_'):
                continue
            
            prop, prop_def, prop_type = self._getPropertyDetailsForName(attr)
            attr = attr.replace('_', '', 1)
            
            regular_value = jsondict.get(attr)
            
            if isinstance(obj, dict):
                # Complex type
                value = prop_type(regular_value)
                value._fromDict(obj)
                    
            elif isinstance(obj, list):
                # Should be a list of dicts
                value = [prop_type(v) for v in regular_value]
                for v, extended_info in zip(value, obj):
                    v._fromDict(extended_info)
            
            value = prop_type(regular_value)
            value._fromDict(obj)
            
            setattr(self, prop.name, value)
            processed.append(attr)
        
        # Then the regular keys/attributes
        for attr, obj in jsondict.items():
            # obj can be dict, list or simple type            
            if attr.startswith('_') or attr in processed:
                continue
                
            prop, prop_def, prop_type = self._getPropertyDetailsForName(attr)
            
            if inspect.isclass(prop_type) and issubclass(prop_type, Resource):
                resourceType = obj.pop('resourceType')
                class_ = eval_type_string(resourceType)
                value = class_()._fromJSON(obj)
            
            elif isinstance(obj, dict):
                # Complex type
                value = prop_type()
                value._fromDict(obj)
                    
            elif isinstance(obj, list):
                # Could be a list of dicts or simple values;
                value = [prop_type()._fromJSON(i) for i in obj]
                
            else:
                value = prop_type(obj)

            setattr(self, prop.name, value)
            
        return self
    # def _fromDict

    def dumps(self, format_='xml'):
        if format_ in SUPPORTED_FORMATS:
            format_ = format_.upper()
            func = getattr(self, 'to' + format_)
            return func()
        
        raise UnsupportedFormatError(format_)
    # def dumps
   
    def toXML(self, parent, path):
        """Return an XML representation of this object."""
        # Iterate over *my* attributes.
        for attr in self._getProperties():
            value = getattr(self, attr)
            desc = getattr(type(self), attr).definition
            path_str = '.'.join(path + [attr, ])
            
            if value is not None:
                if desc.repr == 'xmlAttr':
                    parent.set(attr, str(value))
            
                # elif issubclass(desc.type, xhtml):
                elif desc.repr == 'text':
                    parent.append( ET.fromstring(str(value)) )

                elif isinstance(value, PropertyList):
                    for p in value:
                        p.toXML(ET.SubElement(parent, attr), path + [attr, ])
                        
                elif isinstance(value, FHIRBase):
                    if isinstance(desc.type, list):
                        class_name = upper_first_letter(value.__class__.__name__)
                        attr = attr + class_name
                    value.toXML(ET.SubElement(parent, attr), path + [attr, ])
                
                else:
                    print(value, type(value))
                    raise Exception('unknown property type!?')
        
        # Only the root element needs to generate the actual XML.
        if len(path) == 1:
            x = xml.dom.minidom.parseString(ET.tostring(parent)) 
            pretty_xml = x.toprettyxml(indent='  ')

            if isinstance(self, Element):
                pretty_xml = pretty_xml.replace('<?xml version="1.0" ?>\n', '')
            
            # return ET.tostring(parent)
            return pretty_xml
    # def toXML
    
    def toJSON(self):
        """Return a JSON representation of this object."""
        return json.dumps(self.toDict(), indent=2)
    # def toJSON
    
    def toNative(self):
        return self.toDict()
    # def toNative

    def toDict(self):
        """Return a dictionary representation of this object."""
        # dict in python3 already keeps order
        retval = dict()

        if isinstance(self, Resource):            
            retval['resourceType'] = self.__class__.__name__

        # Iterate over *my* attributes.
        for attr in self._getProperties():
            property_def = getattr(type(self), attr).definition
            value = getattr(self, attr)

            if isinstance(value, BaseType):
                # BaseType: basic type for basic/simple types.
                if isinstance(property_def.type, list):
                    class_name = upper_first_letter(value.__class__.__name__)
                    attr = attr + class_name 

                v = value.toNative()
                if v != None:
                    retval[attr] = v

                json_dict = value.toDict()
                if json_dict:
                    retval['_' + attr] = json_dict
                
            elif isinstance(value, PropertyList):
                # For attributes with cardinality > 1
                listvalues = list()
                _listvalues = list()

                # Iterate over the items in the list
                for v in value:
                    if isinstance(v, BaseType):
                        listvalues.append(v.toNative())
                        _v = v.toDict()
                        if not _v:
                            _v = None
                        _listvalues.append(_v)
                    else:
                        listvalues.append( v.toDict() )
                
                if listvalues:
                    retval[attr] = listvalues

                # Note that '!=' is used here on purpose!
                if sum(map(lambda x: x != None, _listvalues)) > 0:
                    retval['_' + attr] = _listvalues

            elif isinstance(value, FHIRBase):
                # Other Elements and Resources
                if isinstance(property_def.type, list):
                    class_name = upper_first_letter(value.__class__.__name__)
                    attr = attr + class_name 

                json_dict = value.toDict()

                if json_dict:
                    retval[attr] = json_dict
            
        return retval
    # def toDict
# class FHIRBase 

class Element(FHIRBase):
    """Base definition for all elements in a resource."""
    _timestamp = 1548408558
    _url = 'http://hl7.org/fhir/StructureDefinition/Element'
    
    id = Property('id', 'id', '0', '1')
    extension = Property('extension', 'Extension', '0', '*')
    
    def toXML(self, parent=None, path=None):
        """Return an XML representation of this object."""
        if parent is None:
            tag = self.__class__.__name__
            path = [tag, ]
            parent = ET.Element(tag)
        
        return super().toXML(parent, path)
# class Element

class Extension(Element):
    """Optional Extensions Element - found in all resources."""
    _url = 'http://hl7.org/fhir/StructureDefinition/Extension'
    
    url = Property('url', 'uri', '1', '1', 'xmlAttr')
    value = Property(
        'value', 
        ['boolean', 'integer', 'decimal', 'base64Binary', 'instant', 'string', 
            'uri', 'date', 'dateTime', 'time', 'code', 'oid', 'id', 
            'unsignedInt', 'positiveInt', 'markdown', 'Annotation', 'Attachment', 
            'Identifier', 'CodeableConcept', 'Coding', 'Quantity', 'Range', 
            'Period', 'Ratio', 'SampledData', 'Signature', 'HumanName', 'Address', 
            'ContactPoint', 'Timing', 'Reference', 'Meta'], 
        '0', 
        '1'
    )
# class Extension

class Reference(Element):
    """
    A reference from one resource to another.
    
    Autogenerated class.
    """
    _url = 'http://hl7.org/fhir/StructureDefinition/Reference'
    
    reference = Property('reference', 'string', '0', '1')
    identifier = Property('identifier', 'Identifier', '0', '1')
    display = Property('display', 'string', '0', '1')

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._allowed_profiles = args
        self._set(**kwargs)

    def __call__(self, *args, **kwargs):
        # stars(True)
        # print('Reference.__call__', args, kwargs)
        # print('self: ', self)
        # print(f'self.__dict__: {self.__dict__}')
        # stars()
        return self.__class__(*self._allowed_profiles, **kwargs)
# class Reference

class BaseType(Element):
    """Base for basic/simple types."""

    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
    
    def __repr__(self):
        """repr(x) <==> x.__repr__()"""
        return repr(self.value)

    def toNative(self):
        if self.value is None:
            return None
        
        type_ = type(self.value)
        return type_(self.value)
# class BaseType

# ------------------------------------------------------------------------------
# date/time types
# ------------------------------------------------------------------------------

# FHIR types
# ----------
# date: {xs:date, xs:gYearMonth, xs:gYear}
#  - *no* timezone
#  - regex: -?[0-9]{4}(-(0[1-9]|1[0-2])(-(0[0-9]|[1-2][0-9]|3[0-1]))?)?

# time: 
#  - {xs:time}, *no* timezone
#  - regex: ([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?
# 
# dateTime: 
#  - {xs:dateTime, xs:date, xs:gYearMonth, xs:gYear}
#  - timezone *conditional* on population of hours & minutes
#  - regex: -?[0-9]{4}(-(0[1-9]|1[0-2])(-(0[0-9]|[1-2][0-9]|3[0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?
# 
# instant: {xs:dateTime}
#  - timezone *required*
#  - regex: <none>?
class dateTimeBase(BaseType):
    """Base class for date/time classes.
    
    The currently available modules are not capable of storing None values for
    months, days, hours, etc. As a side effect, parsing a string with only a 
    year e.g. strptime('2015', '%Y') automatically sets the month to january!?
    """
    _allowed_attributes = list(FHIRBase._allowed_attributes)
    _allowed_attributes.extend([
        '_value'
    ])

    _regex = None

    def __init__(self, value):
        if value is None or self._checkRegEx(value):
            self._value = value
        super().__init__(value)

    def _checkRegEx(self, value):
        if self._regex and re.match(self._regex, value):
            # The logic below would ideally be implemented by the subclass in
            # question, but this makes generating the subclasses much easier.
            if isinstance(self, dateTime) or isinstance(self, instant):
                p = dateutil.parser.parse(value)
                
                if isinstance(self, dateTime) and (p.hour or p.minute or p.second) and (p.tzinfo is None):
                    args = [value, self.__class__.__name__]
                    raise ValueError('"{}" is not a valid {}'.format(*args))
                
                elif isinstance(self, instant) and (p.tzinfo is None):
                    args = [value, self.__class__.__name__]
                    raise ValueError('"{}" is not a valid {}'.format(*args))
            
            return True
        elif self._regex is None:
            
            return True
        else:
            args = [value, self.__class__.__name__]
            raise ValueError('"{}" is not a valid {}'.format(*args))
            
    def __repr__(self):
        return repr(self._value)
    
    def __str__(self):
        return str(self._value)
# class dateTimeBase 


# Import basic types into module/package 'fhir.model'
from ._markdown import markdown
from ._integer import integer
from ._datetime import dateTime
from ._unsignedint import unsignedInt
from ._code import code
from ._date import date
from ._decimal import decimal
from ._uri import uri
from ._canonical import canonical
from ._url import url
from ._id import id
from ._base64binary import base64Binary
from ._time import time
from ._oid import oid
from ._positiveint import positiveInt
from ._string import string
from ._boolean import boolean
from ._uuid import uuid
from ._instant import instant
from ._xhtml import xhtml

# Import complex types and resources into module/package 'fhir.model'
# from fhir.resource import Resource
from .resource import Resource
from .address import Address
from .annotation import Annotation
from .attachment import Attachment
from .backboneelement import BackboneElement
from .bundle import Bundle
from .codeableconcept import CodeableConcept
from .coding import Coding
from .composition import Composition
from .contactdetail import ContactDetail
from .contactpoint import ContactPoint
from .domainresource import DomainResource
from .dosage import Dosage
from .duration import Duration
from .humanname import HumanName
from .identifier import Identifier
from .medication import Medication
from .medicationrequest import MedicationRequest
from .meta import Meta
from .narrative import Narrative
from .observation import Observation
from .patient import Patient
from .period import Period
from .quantity import Quantity
from .questionnaire import Questionnaire
from .questionnaireresponse import QuestionnaireResponse
from .range import Range
from .ratio import Ratio
from .sampleddata import SampledData
from .signature import Signature
from .timing import Timing
from .usagecontext import UsageContext

# __all__ = []