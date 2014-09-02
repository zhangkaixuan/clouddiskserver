# -*- coding: utf-8 -*-
'''
Created on 2013年9月28日

@author: adrian
'''
import os
import webob
from webob import Request
from webob import Response
from paste.deploy import loadapp
from wsgiref.simple_server import make_server
from proxy.params import HTTPUnauthorized

from services.backend.log.log import Log    
import datetime

from api.settings import AUTH_URL
from api.swift import swiftAPI

#Filter
class AuthFilter():
    def __init__(self,app):
        self.app = app
        pass
    def __call__(self,environ,start_response):
        req = Request(environ)
        self.token = ''
        self.contentType = req.headers.get('Content-Type', '')
        if self.contentType != 'scloud-user':
            userName = req.headers.get('X-Auth-User', '')
            userKey = req.headers.get('X-Auth-Key', '')
            domain = req.headers['domain']
            try:
                self.url, self.token =  swiftAPI.Connection(authurl =AUTH_URL, user = userName, key = userKey, tenant_name =domain )\
                .get_auth()   
                content = userName+' authorized logging in '+str(datetime.datetime.now())
                Log().info(content)    
            except Exception,e:
                content = req.headers.get('X-Auth-User')+' not authorized to login in, please contact with zhoujip@yeah.net '+str(datetime.datetime.now())+str(e)
                Log().error(content)
        else:
            return self.app(environ,start_response)
        
        if self.token:
            req.headers['token'] = self.token
            req.headers['auth_url'] = self.url
            return self.app(environ,start_response)
        else:
            start_response(HTTPUnauthorized,[("Content-type", "text/plain"),])
            return ''
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in LogFilter.factory", global_conf, kwargs
        return AuthFilter