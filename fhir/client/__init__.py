# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib.request
import urllib.parse
import urllib.error

import logging
from pprint import pprint

import fhir.model
from fhir.model import Resource, Bundle

DEFAULT_ENCODING = 'utf-8'

JSON_MIME_TYPES = ['application/json+fhir', 'application/fhir+json']
XML_MIME_TYPES = ['application/xml+fhir', 'application/fhir+xml']

MAPPING_MIME_TYPE_TO_FORMAT = {
    'application/json+fhir': 'json',
    'application/fhir+json': 'json',
    'application/xml+fhir': 'xml',
    'application/fhir+xml': 'xml',
}

MAPPING_FORMAT_TO_MIME_TYPE = {
    'json': 'application/json+fhir',
    'xml': 'application/xml+fhir',
}

SERVERS = {
    'spark': 'http://spark.furore.com/fhir/',
    'grahame_v2': 'http://test.fhir.org/r2/',
    'grahame_v3': 'http://test.fhir.org/r3/',
}

def parse_content_type(content_type):
    """
    Parses an HTTP Content-Type header.
    
    >>> parse_content_type('application/fhir+json; charset=utf-8')
    ('application/fhir+json', {'charset': 'utf-8'})
    """
    if ';' in content_type:
        content_type_list = [item.strip() for item in content_type.split(';')]
        mime_type, *content_type_parameters = content_type_list
        content_type_parameters = dict([param.split('=') for param in content_type_parameters])
    else:
        mime_type = content_args
        content_type_parameters = dict()
    
    return mime_type, content_type_parameters


# ------------------------------------------------------------------------------
# class Client
# ------------------------------------------------------------------------------
class Client(object):
    """
    FHIR Client.

    >>> client = Client('http://spark.furore.com/fhir/')
    >>> client.query('Patient') # doctest: +ELLIPSIS
    <fhir.model.bundle.Bundle object at 0x...>
    """
    
    def __init__(self, URI=None, **kwargs):
        """Instantiate a new FHIR Client."""
        self.log = logging.getLogger('Client')
        
        self.kwargs = kwargs
        self.kwargs['URI'] = URI
        self.kwargs.setdefault('encoding', DEFAULT_ENCODING)
        self.kwargs.setdefault('format', 'xml')
    
    def _getURL(self, *args):
        URI = self.kwargs['URI']
        args = [str(a) for a in args if a is not None]
        return urllib.parse.urljoin(URI, '/'.join(args))
    
    def _getMimeType(self):
        format_ = self.kwargs['format']
        return format_, MAPPING_FORMAT_TO_MIME_TYPE[format_]
        
    def _getHeaders(self, mime_type):
        return {
            'Accept': mime_type,
            'Content-Type': mime_type,
        }
    
    def _createRequest(self, url: str, resource: Resource, method: str, *args, **kwargs) -> urllib.request.Request:
        """Create a Request to the FHIR server."""
        format_, mime_type = self._getMimeType()
        headers = self._getHeaders(mime_type)
        
        query_params = list()
        query_params.extend(kwargs.items())
        query_params.extend(args)
        url_values = urllib.parse.urlencode(query_params)
        
        if url_values:
            url = url + '?' + url_values

        request = urllib.request.Request(
            url=url,
            headers=headers,
            method=method,
        )

        self.log.debug("Creating request:")
        self.log.debug("  url: '{}'".format(url))
        self.log.debug("  method: '{}'".format(method))
        self.log.debug("  headers: '{}'".format(headers))

        if resource is not None:
            request.data = resource.dumps(format_).encode('utf-8'),
        
        return request, format_
    
    def _makeRequest(self, url, resource, method, *args, **kwargs):

        request, format_ = self._createRequest(url, resource, method, *args, **kwargs)
        
        try:
            with urllib.request.urlopen(request) as response:
                data = self._processResponse(response)
                return data, format_
        except urllib.error.HTTPError as e:
            self.log.exception('Could not execute request: HTTP Error {}: {}'.format(e.code, e.msg))
            raise
            
    
    def _processResponse(self, response):
        self.log.debug("Received response:")
        for key, value in response.getheaders():
            self.log.debug("  {}: '{}'".format(key, value))

        content_type = response.getheader('Content-Type')

        if content_type is not None:
            mime_type, content_type_param = parse_content_type(content_type)
            format_ = MAPPING_MIME_TYPE_TO_FORMAT[mime_type]
            default_encoding = self.kwargs['encoding']
        
            charset = content_type_param.get('charset', default_encoding)
            return response.read().decode(charset)
    
    def configure(self, **kwargs):
        """Update the client configuration."""
        self.kwargs.update(kwargs)
    
    def query(self, resource_type: str, *args, **kwargs) -> Bundle:
        """Query the FHIR server for a specific resource type and return a Bundle.
        
        Parameters
        ----------
        resource_type : str
            Resource type to query (e.g. 'Patient')
        *args : list
            List of (key, value) tuples used as query parameters.
        **kwargs : dict
            Dictionary entries used as query parameters. 
        """
        # FIXME: should consider a SQLAlchemy-like approach, where query() 
        #        returns a builder that resolves after calling one() or all()
        url = self._getURL(resource_type)
        data, format_ = self._makeRequest(url, None, 'GET', *args, **kwargs)
              
        return fhir.model.Bundle.loads(data, format_)
        
    def get(self, resource_type: str, id_: str, **kwargs):
        """Retrieve a specific resource instance from the FHIR server.
        
        Parameters
        ----------
        resource_type : str
            Resource type to get (e.g. 'Patient').
        id_ : str
            Logical id of the resource to retrieve.
        **kwargs : dict
            Dictionary entries used as query parameters (e.g. '_format'). 
        """
        url = self._getURL(resource_type, id_)
        data, format_ = self._makeRequest(url, None, 'GET')
        
        class_ = fhir.model.get_type(resource_type)        
        return class_.loads(data, format_)

    def post(self, resource: Resource, update_existing=False) -> Resource:
        """Create a new resource on the FHIR server.
        
        Parameters
        ----------
        resource : Resource
            Resource instance to create on the server.
        update_existing : bool
            Iff True the `id` and `meta` of the provided resource are updated.
        """
        if resource.id is not None:
            raise Exception('Cannot not POST resources with "id" already set!')
        
        url = self._getURL(resource.getType())
        data, format_ = self._makeRequest(url, resource, 'POST')
        
        class_ = resource.__class__
        new_resource = class_.loads(data, format_)
        
        if update_existing:
            resource.id = new_resource.id
            resource.meta = new_resource.meta
        
        return new_resource
        
    def put(self, resource: Resource, update_existing=False) -> Resource:
        """Update a resource on the FHIR server.
        
        Parameters
        ----------
        resource : Resource
            Resource instance to update on the server.
        update_existing : bool
            Iff True the `meta` of the provided resource is updated.
        """
        url = self._getURL(resource.getType(), resource.id)
        data, format_ = self._makeRequest(url, resource, 'PUT')
        
        class_ = resource.__class__
        new_resource = class_.loads(data, format_)
        
        if update_existing:
            resource.meta = new_resource.meta
        
        return new_resource
            
    def save(self, resource: Resource):
        """Save a resource to the FHIR server.
        
        Depending on the situation either a POST or a PUT is performed. When
        POST is used, the resource `id` and `meta` are updated. When PUT is used
        only the `meta` is updated.
        
        Parameters
        ----------
        resource : Resource
            Resource instance to update on the server.
        """
        if resource.id is None:
            self.post(resource, update_existing=True)
        else:
            self.put(resource, update_existing=True)
    
    def delete(self, resource: Resource):
        """Delete a resource on the FHIR server.
        
        Calling this method has no effect on the resource.
        
        Parameters
        ----------
        resource : Resource or str
            Resource instance or logical id to delete on the server.
        """
        url = self._getURL(resource.getType(), resource.id)
        self._makeRequest(url, None, 'DELETE')

    def set_properties(self, cls):
        """Add the properties like 'get', 'post', 'put' and 'query' to a class.
            
        Adding the above properties makes it possible to call them on a 
        particular resource, for example:
        >>> from fhir.model import Patient
        >>> client = Client('http://spark.furore.com/fhir/')
        >>> client.set_properties(fhir.model.Resource)
        >>> Patient.query() # doctest: +ELLIPSIS
        <fhir.model.bundle.Bundle object at 0x...>
        """
        cls.query = QueryProperty(self)
        cls.get = GetProperty(self)
        cls.save = SaveProperty(self)
        cls.delete = DeleteProperty(self)


class PropertyBase(object):
    """Base for properties that use a Client to add functionality to a Resource."""
    
    def __init__(self, client: Client):
        """Create a new instance."""
        self.client = client
    

class QueryProperty(PropertyBase):
    """Property that adds query functionality to a Resource class."""
    
    def __get__(self, instance, owner):
        classname = owner.getType()
        
        def return_method(*args, **kwargs):
            return self.client.query(classname, *args, **kwargs)
        
        return return_method


class GetProperty(PropertyBase):
    """Property that adds get functionality to a Resource class."""
    
    def __get__(self, instance, owner):
        classname = owner.getType()
        
        def return_method(*args, **kwargs):
            return self.client.get(classname, *args, **kwargs)
        
        return return_method


class SaveProperty(PropertyBase):
    """Property that adds save functionality to a Resource instance."""
    
    def __get__(self, instance, owner):
            
        def return_method(*args, **kwargs):
            if instance is None:
                raise Exception('Can only "save" instances, not classes!')
            
            return self.client.save(instance)
        
        return return_method

        
class DeleteProperty(PropertyBase):
    """Property that adds delete functionality to a Resource instance."""
    
    def __get__(self, instance, owner):
            
        def return_method(*args, **kwargs):
            if instance is None:
                raise Exception('Can only "delete" instances, not classes!')
            
            return self.client.delete(instance)
        
        return return_method
        

