# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib.request
import urllib.parse


class Client(object):
    
    def __init__(self, URI='http://spark.furore.com/fhir/'):
        self.URI = URI
        
    def get(self, resource_type, id_=''):
        url = urllib.parse.urljoin(self.URI, resource_type + '/')
        url = urllib.parse.urljoin(url, id_)
        print(url)
        
        with urllib.request.urlopen(url) as response:
           xml = response.read()
          
        return xml.decode('utf-8')
        