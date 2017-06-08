# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib.request
import urllib.parse

import fhir.model

class Client(object):
    
    def __init__(self, URI='http://spark.furore.com/fhir/'):
        self.URI = URI
        
    def get(self, resource_type, id_=''):
        url = urllib.parse.urljoin(self.URI, resource_type + '/')
        url = urllib.parse.urljoin(url, id_)
        print(url)
        
        with urllib.request.urlopen(url) as response:
           xml = response.read().decode('utf-8')
        
        if id_:
            class_ = fhir.model.get_type(resource_type)
        else:
            class_ = fhir.model.Resource
         
        return class_.fromXML(xml)
        