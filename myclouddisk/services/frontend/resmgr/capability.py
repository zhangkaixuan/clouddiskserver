# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response
import json

# from api.keystone.client import Client
# from api.keystone import *

from api.swift.swiftAPI import Connection
from api.api_map import ApiMapping

from api import settings

from rpc import Rpc


from services.backend.log.log import Log    

class CapabilityController():
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.token = ''
        self.userName = ''
        self.userKey = ''
        self.content = ''
        pass
    
    def GET(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()
        
        self.content_type = req.headers.get('url_pattern', '')
        
        resheaders = []

        
        if self.content_type == 'scloud_object':
            self.content = "the supported Data Object Capabilities:\n ['scloud_read_data', 'scloud_read_metadata', 'scloud_create_data', 'scloud_modify_metadata', 'scloud_delete_dataobject']\n"
        if self.content_type == 'scloud_container':
            self.content = "the supported Data Object Capabilities:\n ['scloud_list_children', 'scloud_read_metadata', 'scloud_create_dataobject', 'scloud_create_container', 'scloud_modify_metadata', 'scloud_post_dataobject', 'scloud_delete_container']\n"
        if self.content_type == 'scloud_domain':
            self.content = "the supported Data Object Capabilities:\n ['scloud_list_children', 'scloud_read_metadata', 'scloud_create_domain', 'scloud_delete_domain', 'scloud_read_acl']\n"
        
        
        
        content_length = len(self.content)
        cl = ('content-length', content_length)
        resheaders.append(cl)
        
        start_response("200 OK", resheaders)

        return self.content
        
        
    
    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
        if req.method == 'GET':
            self.GET(environ, start_response)
        if req.method == "HEAD":
            self.HEAD(environ, start_response)
            
        return [self.content]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return CapabilityController(global_conf)
    
    
    
    