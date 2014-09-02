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
from api.swift.swiftAPI import Connection
from api.api_map import ApiMapping
from api import settings
from services.backend.log.log import Log
from api.utils import Utils
from proxy.params import *
from metadata.data_model import DataLogic
import urllib
import struct
    
class DomainController():
    def __init__(self, global_conf):
        self.global_conf = global_conf
    
    def GET(self, environ,start_response):
        req = Request(environ)
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.token = ''
        resheaders = []
        root_id = Utils.getRootContainerId(self.domain)
        if root_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        try:
            kwargs = {'m_parent_id':root_id}
            cons_objs_get = DataLogic().get_by_kwargs(**kwargs)
        
            if len(cons_objs_get) == 0:
                start_response(HTTPNoContent,[("Content-type", "text/plain"),])
                return ''
            #
            #modify by zhangkaixuan
            #
            containers = '[' 
            objects = '['

            for x in range(len(cons_objs_get)):
                if cons_objs_get[x].m_content_type == 'container':
                    #containers.append(cons_objs_get[x].m_name)
                    containers  = containers + cons_objs_get[x].m_name + ','
                elif cons_objs_get[x].m_content_type == 'object':
                    #objects.append(cons_objs_get[x].m_name)
                    objects = objects + cons_objs_get[x].m_name + ','       
            #cons = ('containers',str(containers))
            #objs = ('objects', str(objects))
            #count = ('count', len(cons_objs_get))
            
            if containers != '[':
                containers = containers[:-1]
            if objects != '[':
                objects = objects[:-1]  
            all = containers + "]#" + objects +"]"
            print all    
            param = str(len(all))+'s'                                                 
            bytes = struct.pack(str(param),all)
            self.content = bytes
            #resheaders.append(cons)
            #resheaders.append(objs)
            #resheaders.append(count)
            #
            #modify by zhangkaixuan
            #
            start_response(HTTPOk,resheaders)
            return self.content
        except Exception,e:
            Log().error('GET_DOMAIN by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+' '+str(e))
            start_response(HTTPInternalServerError, resheaders)
            return ''
        
    def HEAD(self, environ,start_response):
        req = Request(environ)
        self.content = ''
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        flag = 1
        resheaders = []
        try:
#             def get_auth(url, user, key, tenant_name=None):
            print self.global_conf['AUTH_URL']
            auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
            
#             first we here get url and token
            dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
            url, token = ApiMapping().scloud_get_auth(**dic)
            
#             we send the url and token to the api params
            dic = {"storage_url":url, 'token':token}
            resbody= ApiMapping().scloud_head_domain(**dic)
            
#             resbody=  (Connection(authurl =auth_url, user = self.userName,\
#                             key = self.userKey, tenant_name = req.headers['domain']).head_account())
            log_dic = {"log_flag":"info", "content":'HEAD_DOMAIN by '+self.userName+': '+self.domain}
            self.rpc.cast('logs', json.dumps(log_dic)) 

            for value in resbody:
                x = (value,resbody[value])
                resheaders.append(x)
#                 print value
            print resheaders
#             print token
#             self.token = token
#             print self.token, self.userKey, self.userName
        except Exception,e:
            flag = 0
            log_dic = {"log_flag":"error", "content":'HEAD_DOMAIN by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+' '+str(e)}
            self.rpc.cast('logs', json.dumps(log_dic)) 
            
        if flag:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            start_response("200 OK", [])
#             return ["you are not authenticated"]
        
        return ''
        
    
    
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
        return DomainController(global_conf)
    
    
    
    