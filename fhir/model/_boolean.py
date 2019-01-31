# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime as dt
import logging

from . import Property, DateTimeProperty, BaseType, dateTimeBase

__all__ = ['boolean', ]

class boolean_(int):
    def __repr__(self):
        if self:
            return "true"
        else:
            return "false"
    
    __str__ = __repr__

class boolean(BaseType):
    """Adapted from https://www.python.org/dev/peps/pep-0285/"""
    
    value = Property('value', boolean_, '1', '1', 'xmlAttr')
    
    def __init__(self, value):
        if value == "true":
            value = 1
        elif value == "false":
            value = 0
        
        super(boolean, self).__init__(value)
    
    def __repr__(self):
        if self.value:
            return "true"
        else:
            return "false"

    __str__ = __repr__

    def __eq__(self, other):
        if self.value is None or other is None:
            return self.value is None and other is None

        return bool(int(self.value) == int(other))

    def __and__(self, other):
        if isinstance(other, bool) or isinstance(other, boolean):
            return bool(int(self.value) & int(other))
        else:
            return int.__and__(self, other)

    __rand__ = __and__

    def __or__(self, other):
        if isinstance(other, bool):
            return bool(int(self.value) | int(other))
        else:
            return int.__or__(self, other)

    __ror__ = __or__

    def __xor__(self, other):
        if isinstance(other, bool):
            return bool(int(self.value) ^ int(other))
        else:
            return int.__xor__(self.value, other)

    __rxor__ = __xor__
    
    def toNative(self):
        """Overrides BaseType.toNative()."""
        return bool(self.value)
    
    


