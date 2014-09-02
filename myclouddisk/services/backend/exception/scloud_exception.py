# -*- coding: utf-8 -*-
'''
Created on 2013年12月3日

@author: adrian
'''
from exceptions import Exception

class APIException(Exception):
    """
    This exception means we got Exception when we call cloud APIs.
    """

    def __init__(self, reason):
        self.reason = reason

    def __repr__(self):
        return 'Cloud_API: %s' % self.reason

    def __str__(self):
        return 'Cloud_API: %s' % self.reason

class ImportException(Exception):
    """
    This exception means we got Exception when we import
    a job plan xml file.
    """
    def __init__(self, configname):
        self.configname = configname

    def __repr__(self):
        return 'Import configuration Error from %s!'%self.configname

    def __str__(self):
        return 'Import configuration Error from %s!'%self.configname

class NotImplementedError(Exception):
    """
    This Exception means we call an unimplemented API.
    """
    def __init__(self, APIname):
        self.APIname = APIname

    def __repr__(self):
        return 'Not implemented API: %s'%self.APIname

    def __str__(self):
        return 'Not implemented API: %s'%self.APIname

class HTTPLinkDownError(Exception):
    def __str__(self):
        return 'HTTP link is down'