# -*- coding: utf-8 -*-
'''
Created on 2013年10月10日

@author: adrian
'''
import sys
import os
import webob
from webob import Request
from webob import Response
from paste.deploy import loadapp
import httplib, urllib
# for server 
reload(sys)
sys.setdefaultencoding("utf-8")
#zhangkaixuan
from proxy.params import HTTPOk
from proxy.params import HTTPBadRequest
from proxy.params import HTTPMethodNotAllowed

class ControllerFilter():
    def __init__(self,app):
        self.app = app
        pass
    def __call__(self,environ,start_response):
        '''
        controller here to parse user's http request
        '''
        #use webob to pack the environment value
        req = Request(environ)
        req.headers['http-flag'] = HTTPOk
        self.content_type = req.headers.get('Content-Type', '')
        self.host = req.headers.get('Host', '')
        self.cdmi_version = req.headers.get('X-CDMI-Specification-Version', '')
        self.authorization = req.headers.get('Authorization', '')
        self.date = req.headers.get('Date', '')
        self.path = req.path
        req.headers['X-Auth-User'], req.headers['X-Auth-Key'] = self.authorization.strip().split(':')
        
        #Make sure req.headers not ""
        if not (self.content_type and self.host and self.cdmi_version and 
                self.date and self.authorization and req.headers['X-Auth-User'] and 
                req.headers['X-Auth-Key']) or self.content_type not in ['scloud-domain', 'scloud-container', 'scloud-object', 'scloud-capability', 'scloud-user']:
            req.headers['http-flag'] = HTTPBadRequest
            start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
            return ''
        quoted_path = urllib.unquote(str(req.path)).decode("UTF-8")
        
        print 'quoted_path',quoted_path
        #
        #modify by zhangkaixuan
        #        
        x_url_path = quoted_path.strip('/').split('/')
        if(req.method == 'POST'):
            req.headers['current-name'] = x_url_path[-1]
            url_path = x_url_path[0:-1]
        else:
            url_path = quoted_path.strip('/').split('/')
        #
        #modify by zhangkaixuan
        #                    
        req.headers['url_pattern'] = url_path[0]
        
        if req.headers['url_pattern']=='scloud_domain':
            domain = req.headers['domain'] = req.headers['X-Auth-User']
            if domain.strip()=='':
                start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
                return ''
            return self.app(environ,start_response)
        elif req.headers['url_pattern'] == 'scloud_container':
            domain = req.headers['domain'] = req.headers['X-Auth-User']
            container = req.headers['container'] = url_path[1:]
            if domain.strip()=='' or not container :
                start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
                return ''
            return self.app(environ,start_response)
        elif req.headers['url_pattern'] == 'scloud_object':
            domain = req.headers['domain'] = req.headers['X-Auth-User']
            if len(url_path) == 2:
                container = req.headers['container'] = []
                obj = req.headers['object'] = url_path[-1]
            elif len(url_path) > 2:
                container = req.headers['container'] = url_path[1:-1]
                obj = req.headers['object'] = url_path[-1]
            else:
                start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
                return ''
            if domain.strip()=='' or obj.strip()=='':
                start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
                return ''
            return self.app(environ,start_response)
        elif req.headers['url_pattern'] == 'scloud_user':
            return self.app(environ,start_response)
        elif req.headers['url_pattern'] == 'scloud_extra':
            domain = req.headers['domain'] = req.headers['X-Auth-User']
            if domain.strip()=='' or quoted_path.strip()=='':
                start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
                return ''
            return self.app(environ,start_response)
        else:
            start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
            return ''
        
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in LogFilter.factory", global_conf, kwargs
        return ControllerFilter
