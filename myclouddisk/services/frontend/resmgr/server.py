# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response

from obj import ObjectController
from container import ContainerController
from domain import DomainController
from capability import CapabilityController
from services.frontend.usermgr.user import UserController


class ResourceServer():
    
    def __init__(self, global_conf):
        #value requrired
        self.global_conf = global_conf

        #Init four controllers
        self.domain_controller = DomainController(global_conf)
        self.obj_controller = ObjectController(global_conf)
        self.container_controller = ContainerController(global_conf)
        self.capability_controller = CapabilityController(global_conf)
        self.user_controller = UserController(global_conf)
        
    
    def GET(self, environ,start_response):
        
        if self.content_type == 'scloud-domain':
            self.content = self.domain_controller.GET(environ, start_response)
        if self.content_type == 'scloud-container':
            self.content = self.container_controller.GET(environ, start_response)
        if self.content_type == 'scloud-object':
            self.content = self.obj_controller.GET(environ, start_response)
        if self.content_type == 'scloud-capability':
            self.content = self.capability_controller.GET(environ, start_response)
        
    def HEAD(self, environ,start_response):
        if self.content_type == 'scloud-domain':
            self.content = self.domain_controller.HEAD(environ, start_response)
        if self.content_type == 'scloud-container':
            self.content = self.container_controller.HEAD(environ, start_response)
        if self.content_type == 'scloud-object':
            self.content = self.obj_controller.HEAD(environ, start_response)
        
    def POST(self, environ,start_response):
#         if self.content_type == 'scloud-domain':
#             self.content = self.domain_controller.HEAD(environ, start_response)
        if self.content_type == 'scloud-container':
            self.content = self.container_controller.POST(environ, start_response)
        if self.content_type == 'scloud-object':
            self.content = self.obj_controller.POST(environ, start_response)
        
    def PUT(self, environ,start_response):
#         if self.content_type == 'scloud-domain':
#             self.content = self.domain_controller.HEAD(environ, start_response)
        if self.content_type == 'scloud-container':
            self.content = self.container_controller.PUT(environ, start_response)
        if self.content_type == 'scloud-object':
            self.content = self.obj_controller.PUT(environ, start_response)
        if self.content_type == 'scloud-user':
            self.content = self.user_controller.PUT(environ, start_response)
        
    def DELETE(self, environ,start_response):
#         if self.content_type == 'scloud-domain':
#             self.content = self.domain_controller.HEAD(environ, start_response)
        if self.content_type == 'scloud-container':
            self.content = self.container_controller.DELETE(environ, start_response)
        if self.content_type == 'scloud-object':
            self.content = self.obj_controller.DELETE(environ, start_response)
        
    
    def _get_headers(self, req):
        self.http_status = req.headers['http-flag']
        #here content type includes scloud-object, scloud-domain, scloud-container, scloud-capability
        #later we may add scloud-queue type
        self.content_type = req.headers.get('Content-Type', '')
        #DomainName.scloud.ecust.com
        self.host = req.headers.get('Host', '')
        self.cdmi_version = req.headers.get('X-CDMI-Specification-Version', '')
        self.authorization = req.headers.get('Authorization', '')
        self.date = req.headers.get('Date', '')
        self.path = req.path
    
    
    def __call__(self,environ,start_response):
        req = Request(environ)
        self._get_headers(req)
        
        if req.method == 'GET':
            self.GET(environ, start_response)
        if req.method == "HEAD":
            self.HEAD(environ, start_response)
        if req.method == "PUT":
            self.PUT(environ, start_response)
        if req.method == "DELETE":
            self.DELETE(environ, start_response)
        if req.method == "POST":
            self.POST(environ, start_response)
            
        return [self.content]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return ResourceServer(global_conf)
    
    
    
    