# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日
@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response
import hashlib 
import datetime
from proxy.params import *
from services.backend.log.log import Log

from api.settings import AUTH_URL
from api.keystone import client
from api.swift import swiftAPI
from metadata.data_model import DataLogic

class UserController():
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self.token = ''
        self.userName = ''
        self.userKey = ''
        self.content = ''
        
    def PUT(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        name = self.userName = req.headers.get('X-Auth-User', '').strip()
        password = self.userKey = req.headers.get('X-Auth-Key', '').strip()
        email = self.email = req.headers.get('email', '').strip()
        Log().info("start user PUT operation username:"+self.userName)
                
        try:
            aus = client.Client(auth_url=AUTH_URL)
            users = [n.name for n in aus.users.findall()]
            tenants = [n.name for n in aus.tenants.findall()] 
            
            if name not in users and name not in tenants:
                tenant_id = aus.tenants.create(name, 'name the same as the user name', True).id
                user_id = aus.users.create(name, password, email, tenant_id, True).id
    #            aus.roles.
                conn = swiftAPI.Connection(authurl = AUTH_URL,user = name,key = password,tenant_name = name)
                admin_role_id = ''
                for role in aus.roles.findall():
                    if role.name == 'admin':
                        admin_role_id = role.id
                aus.roles.add_user_role(user_id, admin_role_id, tenant_id)
                #when creating a user also create three folders for this user as files, pictures, videos
                root_container = name+"root"
                root_contaienr_md5 = hashlib.md5(root_container).hexdigest() 
                conn.put_container(root_contaienr_md5)
                kwargs = {
                                'm_name' : 'root_container',
                                'm_storage_name' : root_contaienr_md5,
                                'm_domain_name' : name,
                                'm_content_type' : 'container',
                                'm_status' : '1',   #'1' means available, '0' means not available
                                'm_uri' : '/',
                                'm_hash' : '' ,
                                'm_size' : '',
                                'm_parent_id' : 0,
                                'created' : str(datetime.datetime.now()),
                    }      
                DataLogic().add_data(**kwargs);
            else:
                Log().warning("user:"+name+" already existing")
                start_response(HTTPConflict,[("Content-type", "text/plain"),])
                return self.content
        except Exception , e:
            Log().error(str(e))
            start_response(HTTPInternalServerError,[("Content-type", "text/plain"),])
            return self.content
        start_response(HTTPCreated,[("Content-type", "text/plain"),])
        return self.content
    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
        if req.method == "PUT":
            self.PUT(environ, start_response)
            
        return [self.content,]
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return UserController(global_conf)