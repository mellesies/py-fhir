# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime as dt
import logging

from . import Property, DateTimeProperty, BaseType, dateTimeBase

__all__ = ['positiveInt', ]

class positiveInt(BaseType):
    """Autogenerated positiveInt type."""
    
    value = Property('value', int, '1', '1', 'xmlAttr')
    
    def __init__(self, value=None):
        """Initialize a new positiveInt instance."""
        if value is not None:
            value = int(value)

        super(positiveInt, self).__init__(value)
    
    def __int__(self):
        return int(self.value)

    def __eq__(self, other):
        if self.value is None or other is None:
            return self.value is None and other is None
        if isinstance(other, positiveInt):
            return self.value.__eq__(other.value)
        elif isinstance(other, int):
            return self.value.__eq__(other)
        
        return self.value.__eq__(other)
        
    def __ne__(self, other):
        if self.value is None or other is None:
            return not (self.value is None and other is None)
        if isinstance(other, positiveInt):
            return self.value.__ne__(other.value)
        elif isinstance(other, int):
            return self.value.__ne__(other)
        
        return self.value.__ne__(other)
        
    def __lt__(self, other):
        if isinstance(other, positiveInt):
            return self.value.__lt__(other.value)
        elif isinstance(other, int):
            return self.value.__lt__(other)
        
        return self.value.__lt__(other)
        
    def __le__(self, other):
        if isinstance(other, positiveInt):
            return self.value.__le__(other.value)
        elif isinstance(other, int):
            return self.value.__le__(other)
        
        return self.value.__le__(other)
        
    def __gt__(self, other):
        if isinstance(other, positiveInt):
            return self.value.__gt__(other.value)
        elif isinstance(other, int):
            return self.value.__gt__(other)
        
        return self.value.__gt__(other)
        
    def __ge__(self, other):
        if isinstance(other, positiveInt):
            return self.value.__ge__(other.value)
        elif isinstance(other, int):
            return self.value.__ge__(other)
        
        return self.value.__ge__(other)
        
    def __add__(self, other):
        if isinstance(other, positiveInt):
            return positiveInt(self.value.__add__(other.value))
        elif isinstance(other, int):
            return self.value.__add__(other)
        
        return self.value.__add__(other)
        
    __radd__ = __add__
    
    
    def __div__(self, other):
        """x / y <==> x.__div__(y)"""
        if isinstance(other, int) or isinstance(other, positiveInt):
            return positiveInt(int(self).__div__(int(other)))
            
        return other.__rdiv__(int(self))

    def __rdiv__(self, other):
        """y / x <==> x.__rdiv__(y)"""
        if isinstance(other, int) or isinstance(other, positiveInt):
            return positiveInt(int(self).__rdiv__(int(other)))
            
        return other.__div__(int(self))
    
    def __mul__(self, other):
        """x * y <==> x.__mul__(y)"""
        if isinstance(other, int) or isinstance(other, positiveInt):
            return positiveInt(int(self).__mul__(int(other)))
            
        return other.__mul__(int(self))

    def __rmul__(self, other):
        """y * x <==> x.__rmul__(y)"""
        if isinstance(other, int) or isinstance(other, positiveInt):
            return positiveInt(int(self).__mul__(int(other)))
            
        return other.__rmul__(int(self))


