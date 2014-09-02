# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''

import os
import webob
from webob import Request
from webob import Response
from services.backend.log.log import Log
from api.api_map import ApiMapping

from metadata.domain_model import DomainLogic
from metadata.data_model import DataLogic
from api.utils import Utils
from proxy.params import *
import datetime
import hashlib
import re

class ObjectController():
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
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.object = req.headers.get('object', '')
        self.size = req.headers.get('content-length', '')
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        
        Log().info("start object GET operation username:"+self.userName+",domain:"+self.domain+",container:"+str(containers_object)+
                   ",object:"+self.object)
        
        c_len = len(containers_object)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        resheaders = []
        for i in xrange(c_len):
            c_name = containers_object[i].encode("UTF-8")
            kwargs = {'m_name':c_name, 'm_parent_id':parent_id}
            containers_object_get = DataLogic().get_by_kwargs(**kwargs)
            if len(containers_object_get) == 0:
                if i == c_len-1:
                    Log().error('can not get the object ['+c_name+"] id")
                    start_response(HTTPNotFound,[("Content-type", "text/plain"),])
                    return ''
                else:
                    Log().error('can not get the container ['+c_name+"] id")
                    start_response(HTTPNotFound,[("Content-type", "text/plain"),])
                    return ''
                break
            else:
                if i == c_len-1:
                    self.object = containers_object_get[0].m_storage_name
                else:
                    self.container = containers_object_get[0].m_storage_name
                parent_id = containers_object_get[0].id
        try:
            token = req.headers['token']
            url = req.headers['auth_url']
            dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
                   'object':self.object,}
            headers, body = ApiMapping().scloud_get_object(**dic)
            print "++++++++DFDF",type(body)  
            self.content = body
            #print self.content
            Log().info('GET_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
            for value in headers:
                x = (value,headers[value])
                resheaders.append(x)
#             resheaders.get('Content-Type', 'application/octet-stream')
            start_response(HTTPOk, resheaders)
            return self.content
        except Exception,e:
            Log().error('GET_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
            start_response(HTTPInternalServerError, resheaders)
            return self.content
    def HEAD(self, environ,start_response):
        
        self.content = ''

#         req = Request(environ)
#         self.userName = req.headers.get('X-Auth-User', '')
#         self.userKey = req.headers.get('X-Auth-Key', '')
#         self.domain = req.headers.get('domain', '')
#         self.object = req.headers.get('object', '')
#         self.rpc = Rpc()
#         containers_object = req.headers.get('container','')
#         containers_object.append(str(self.object))
#         print containers_object
#         c_len = len(containers_object)# the length of the container
# 
#         #modified by adrian
#         #use rabbit to diliver message
#         kwargs = {'metadata_target':'domain', 'name':self.domain, 'metadata_opr':'get'}
#         domains_get = self.rpc.call('meta_queue', **kwargs)
#         domains_dic = json.loads(domains_get)
#         
#         parent_id = domains_dic[0].get('id', '')
#         
#         if parent_id == '':
#             req.headers['http-flag'] = HTTPInternalServerError
#             log_dic = {"log_flag":"error", "content":'can not get the domain ['+self.domain+"] id"}
#             self.rpc.cast('logs', json.dumps(log_dic))
# 
# #         parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
#          
#         resheaders = []
#         info = '200 OK'
#         
#         for i in xrange(c_len):
#             c_name = containers_object[i]
#             print parent_id
#             kwargs = {'metadata_target':'data', 'm_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id}
#             containers_object_get = self.rpc.call('meta_queue', **kwargs)
#             containers_object_dic = json.loads(containers_object_get)
#             
#             #get the container name
#             
#             if len(containers_object_dic) == 0:
#                 if i == c_len-1:
#                     info = '404 Object Not Found'
#                 else:
#                     info = '404 Container Not Found'
#                 break
#             else:
#                 if i == c_len-1:
#                     self.object = containers_object_dic[0].get('m_storage_name', '')
#                 else:
#                     self.container = containers_object_dic[0].get('m_storage_name', '')
#                     
#                 parent_id = containers_object_dic[0].get('id','')
#                 
#         if info == '200 OK':
#             try:
#                 auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
#                 
#                 dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
#                 url, token = ApiMapping().scloud_get_auth(**dic)
#                  
#                 dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
#                        'object':self.object,}
#                 
#                 headers = ApiMapping().scloud_head_object(**dic)
#  
# #             headers,body=  (Connection(authurl =auth_url, user = self.userName,\
# #                             key = self.userKey, tenant_name = req.headers['domain']).get_object(req.headers['container'], req.headers['object']))
#                 log_dic = {"log_flag":"info", "content":'HEAD_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object}
#                 self.rpc.cast('logs', json.dumps(log_dic))
#                 
# #                 here is something that will be excuted after
# #                 这里的response不支持content-length，后面需要解决这个问题！
#                 
#                 for item in headers.items():
#                     if item[0]!= 'content-length':
#                         resheaders.append(item)
#                         
#                     
#                 print resheaders
#      
#                  
#             except Exception,e:
#                 info = '404 Object Not Found'
#                 print e
#                 log_dic = {"log_flag":"error", "content":'HEAD_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+self.container+'/'+req.headers['object']+' '+str(e)}
#                 self.rpc.cast('logs', json.dumps(log_dic))
#                 print sys.exc_info()
        info = 'success' 
        start_response(info, [ ('accept-ranges', 'bytes'), ('last-modified', 'Mon, 04 Nov 2013 14:42:02 GMT'), ('etag', 'd7d1c51fb2ea6a8d59bd3922f33bf7a7'), ('x-trans-id', 'tx8fadb8db0ea9465c83a0fdb00fa7fb58'), ('date', 'Mon, 04 Nov 2013 14:43:24 GMT'), ('content-type', 'application/octet-stream')])
         
        return self.content
        

        
    def PUT(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        containers = req.headers.get('container','')
        self.object = req.headers.get('object', '').encode("UTF-8")
        self.size = req.headers.get('content-length', '')
        
        c_len = len(containers)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        
        if c_len == 0:
            self.container = Utils.getRootContainerStorageName(self.domain)
        resheaders = []
        Log().info("start object PUT operation username:"+self.userName+",domain:"+self.domain+",containers:"+str(containers)+
                   ",object:"+self.object)        
        for i in xrange(c_len):
            c_name = containers[i].encode("UTF-8")
            kwargs = {'m_name':c_name, 'm_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = DataLogic().get_by_kwargs(**kwargs)
            if len(containers_get) == 0:
                Log().error('Containers not Found, PUT_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container']))
                start_response(HTTPNotFound, resheaders)
                return self.content  
            else:
                self.container = containers_get[0].m_storage_name
                parent_id = containers_get[0].id
                
        kwargs = {'m_name':self.object, 'm_parent_id':parent_id, 'm_content_type':'object'}
        object_get = DataLogic().get_by_kwargs(**kwargs)
        
        if len(object_get) > 0:
            kws = {'id':object_get[0].id}
            object_get = DataLogic().delete_data_by_id(**kws)
        try:
            Log().info('START PUT_OBJECT by '+self.userName+': '+self.domain+'/'+str(containers)+'/'+self.object)

            token = req.headers['token']
            url = req.headers['auth_url']
            sfile = req.body_file
            #transaction control
            object_name_construct = self.userName+'_'+str(parent_id)+'_'+self.object+'_'+self.domain+'_'+'object_'+"".join(re.split('\W+', str(datetime.datetime.now())))
            object_storagename = hashlib.md5(object_name_construct).hexdigest()  
             
            dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
                   'object':object_storagename, 'contents':sfile}
            object_hash = ApiMapping().scloud_put_object(**dic)
            kwargs = {
                            'm_name' : self.object,
                            'm_storage_name' : object_storagename,
                            'm_domain_name' : self.domain,
                            'm_content_type' : 'object',
                            'm_status' : '1',   #'1' means available, '0' means not available
                            'm_uri' : object_storagename,
                            'm_hash' : object_hash ,
                            'm_size' : '2G',
                            'm_parent_id' : parent_id,
                            'created' : str(datetime.datetime.now()),
                }      
            DataLogic().add_data(**kwargs);
            for item in kwargs.items():
                resheaders.append(item)
            start_response(HTTPCreated, resheaders)
            return self.content
        except Exception,e:
            Log().error('PUT_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
            start_response(HTTPInternalServerError, resheaders)
            return ''
         
    def DELETE(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.object = req.headers.get('object', '')
        self.size = req.headers.get('content-length', '')
        containers_object = req.headers.get('container','')
        containers_object.append(str(self.object))
        Log().info("start object GET operation username:"+self.userName+",domain:"+self.domain+",container:"+str(containers_object)+
                   ",object:"+self.object)
        c_len = len(containers_object)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        resheaders = []
        for i in xrange(c_len):
            c_name = containers_object[i].encode("UTF-8")
            kwargs = {'m_name':c_name, 'm_parent_id':parent_id}
            containers_object_get = DataLogic().get_by_kwargs(**kwargs)
            if len(containers_object_get) == 0:
                if i == c_len-1:
                    Log().error('can not get the object ['+c_name+"] id")
                    start_response(HTTPNotFound,[("Content-type", "text/plain"),])
                    return ''
                else:
                    Log().error('can not get the container ['+c_name+"] id")
                    start_response(HTTPNotFound,[("Content-type", "text/plain"),])
                    return ''
                break
            else:
                if i == c_len-1:
                    self.object = containers_object_get[0].m_storage_name
                else:
                    self.container = containers_object_get[0].m_storage_name
                parent_id = containers_object_get[0].id
        try:
            Log().info('START DELETE_OBJECT by '+self.userName+': '+self.domain+'/'+self.container+'/'+self.object)
            token = req.headers['token']
            url = req.headers['auth_url']
            dic = {"storage_url":url, 'token':token, 'container':self.container,'headers':{}, \
                   'object':self.object,}
            ApiMapping().scloud_delete_object(**dic)
            kwargs = {
                        'id': parent_id,
                }      
            DataLogic().delete_data_by_id(**kwargs)
            start_response(HTTPOk, [("Content-type", "text/plain"),])
            return ''
        except Exception,e:
            Log().error('DELETE_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
            start_response(HTTPInternalServerError, resheaders)
            return ''
    
    def POST(self, environ,start_response):
        
        '''POST can be used to change object metadata
        object rename
        '''
        self.content = ''
        req = Request(environ)
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        self.original_name = req.headers.get('object','').encode("UTF-8")
        self.current_name = req.headers.get('current-name','').encode("UTF-8")
        
        containers = req.headers.get('container','')
        Log().info("start object POST operation username:"+self.userName+",domain:"+self.domain+",container:"+str(containers)+",original-name:"+self.original_name+",current-name:"+self.current_name)  
        c_len = len(containers)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        resheaders = []
        if self.current_name == '':
            start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
            return 'current_name not assigned\n'
        for i in xrange(c_len):
            c_name = containers[i].encode("UTF-8")
            # get all the containers corresponding to such conditions    
            kwargs = {'m_name':c_name, 'm_parent_id':parent_id,  'm_content_type':'container'}
            containers_get = DataLogic().get_by_kwargs(**kwargs)
            if len(containers_get) != 0:
                parent_id = containers_get[0].id
                if i == c_len-1:
                    try:
                        kws = {'m_name':self.original_name, 'm_parent_id':parent_id, 'm_content_type':'object'}
                        o_get = DataLogic().get_by_kwargs(**kws)
                        object_id = o_get[0].id
                        kwsExisting = {'m_name':self.current_name, 'm_parent_id':parent_id, 'm_content_type':'object'}
                        o_get_2 = DataLogic().get_by_kwargs(**kwsExisting)
                        if len(o_get_2) == 0:
                            kwargs = {'id':object_id, 'm_name':self.current_name}
                            DataLogic().update_data_by_id(**kwargs)
                            start_response(HTTPOk, resheaders)
                            return self.content
                        else:
                            start_response(HTTPConflict, resheaders)
                            return self.content
                    except Exception,e:
                        Log().error('POST_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                        start_response(HTTPInternalServerError, resheaders)
                        return self.content
            else:
                Log().error('Containers not Found, POST_OBJECT by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container']))
                start_response(HTTPNotFound, resheaders)
                return self.content    
    def __call__(self,environ,start_response):
        
        req = Request(environ)
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
            
        return [self.content,]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return ObjectController(global_conf)
    
    
    
    
