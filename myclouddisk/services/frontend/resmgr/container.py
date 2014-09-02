# -*- coding: utf-8 -*-
'''
Created on 2013年9月22日

@author: adrian
'''
import os
import webob
from webob import Request
from webob import Response
from proxy.params import *
import json
from api.api_map import ApiMapping
from metadata.data_model import DataLogic
from metadata.domain_model import DomainLogic
from api.swift.swiftAPI import Connection
from api import settings
from services.backend.log.log import Log
import datetime
import re
import hashlib
from api.utils import Utils
from api.settings import  AUTH_URL
import struct


    
class ContainerController():
    '''
    对于container的操作这里包含四个：
    PUT, GET, HEAD, DELETE, POST
    
    这里使用metadata封装数据，实现了文件夹的嵌套功能。
    
    对于PUT操作，如果url中的container不存在，程序将建立一个文件夹，注意一个PUT操作一次最多只能建立一个文件夹。
    对于GET, HEAD, DELETE, POST，如果url路径中的container不存在，则将报出404 Container NOT Found的错误
    api使用scloud标准api
    '''
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
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        resheaders = []
        for i in xrange(c_len):
            c_name = containers[i].encode("UTF-8")
            kwargs = {'m_name':c_name,'m_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = DataLogic().get_by_kwargs(**kwargs)
            if len(containers_get) != 0:
                parent_id = containers_get[0].id
                if i == c_len-1:
                    try:
                        kwargs = {'m_parent_id':parent_id}
                        cons_objs_get = DataLogic().get_by_kwargs(**kwargs)
                        if len(cons_objs_get) == 0:
                            start_response(HTTPNoContent,[("Content-type", "text/plain"),])
                            return ''
                        #
                        #modify by zhangkaixuan
                        #
                        #containers = []
                        #objects = []
                        containers = '['
                        objects = '['
                        for x in range(len(cons_objs_get)):
                            if cons_objs_get[x].m_content_type == 'container':
                                #containers.append(cons_objs_get[x].m_name.decode("UTF-8"))
                                containers  = containers + cons_objs_get[x].m_name + ','
                            elif cons_objs_get[x].m_content_type == 'object':
                                #objects.append(cons_objs_get[x].m_name.decode("UTF-8"))
                                objects = objects + cons_objs_get[x].m_name + ','
                                
#                         cons = ('containers',str(containers))
#                         objs = ('objects', str(objects))
#                         count = ('count', len(cons_objs_get))
#                         resheaders.append(cons)
#                         resheaders.append(objs)
#                         resheaders.append(count)                                              
                        if containers != '[':
                            containers = containers[:-1]
                        if objects != '[':
                            objects = objects[:-1]
                
                        all = containers + "]#" + objects +"]"                        
                        param = str(len(all))+'s'                                                
                        bytes = struct.pack(str(param),all)                                   
                        self.content = bytes
                        start_response(HTTPOk,resheaders)
                        #
                        #modify by zhangkaixuan
                        #                      
                        return  self.content
                    except Exception,e:
                        Log().error('GET_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                        start_response(HTTPInternalServerError, resheaders)
                        return ''
            else:
                Log().error('Containers not Found, DELETE_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container']))
                start_response(HTTPNotFound, resheaders)
                return self.content  
            
        
    def HEAD(self, environ,start_response):
        self.content = ''
        req = Request(environ)
        res = Response()

        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')

        
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        
        
        #modified by adrian
        #use rabbit to diliver message
        kwargs = {'metadata_target':'domain', 'name':self.domain, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        
        parent_id = domains_dic[0].get('id', '')
        
        if parent_id == '':
            req.headers['http-flag'] = HTTPInternalServerError
            log_dic = {"log_flag":"error", "content":'can not get the domain ['+self.domain+"] id"}
            self.rpc.cast('logs', json.dumps(log_dic))           
#         parent_id = DomainLogic().get_by_kwargs(**{'name':self.domain})[0].id
        
        flag = 1
        resheaders = []
        
#         这里我们将遍历url中的所有的container
        
        for i in xrange(c_len):
            c_name = containers[i].encode("UTF-8")
            
            # get all the containers corresponding to such conditions    
            kwargs = {'metadata_target':'data', 'm_name':c_name, 'metadata_opr':'get', 'm_parent_id':parent_id,  'm_content_type':'container'}
            containers_get = self.rpc.call('meta_queue', **kwargs)
            containers_dic = json.loads(containers_get)
            
            if len(containers_dic) != 0:
                parent_id = containers_dic[0].get('id','')
                storage_name = containers_dic[0].get('m_storage_name', '')

                if i == c_len-1:
                    try:
            #             def get_auth(url, user, key, tenant_name=None):
                        print self.global_conf['AUTH_URL']
                        auth_url =  str(self.global_conf['AUTH_URL']).strip("'")
                        
                        dic = {"auth_url":auth_url, 'user':self.userName, 'key':self.userKey, 'domain_name':self.domain}
                        url, token = ApiMapping().scloud_get_auth(**dic)
                        
                        dic = {"storage_url":url, 'token':token, 'container':storage_name,'headers':{}}
#                         ApiMapping().scloud_put_container(**dic)
#                         ApiMapping().scloud_delete_container(**dic)
                        resbody = ApiMapping().scloud_head_container(**dic)
                        log_dic = {"log_flag":"info", "content":'GET_CONTAINER by '+self.userName+': '+self.domain+'/'+c_name}
                        self.rpc.cast('logs', json.dumps(log_dic)) 
            
                        
                        for value in resbody:
                            x = (value,resbody[value])
                            resheaders.append(x)
            #                 print value
                        print resheaders
                        break
                        
                    except Exception,e:
                        flag = 0
                        log_dic = {"log_flag":"error", "content":'PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e)}
                        self.rpc.cast('logs', json.dumps(log_dic)) 
                        break
            else:
                print 'Containers not Found'
                flag = 0

        
        if flag:
            start_response("200 OK", resheaders)
#             return [str(contianers_in_account),]
        else:
            start_response("404 Container Not Found", [])
#             return ["you are not authenticated"]
        
        return self.content        
        
        
    def PUT(self, environ,start_response):
        '''
            the url curl   -i -H "X-Auth-Key: ADMIN"  -H "X-Auth-User: admin" 
             http://localhost:8080/scloud_container/domain/c1/c2/c3/c4   -X PUT
            this PUT method will only find the first not existing container then creat it.
            will Ignore the others containers which does not exist.
            and returns the metadata of the new container
        '''
        self.content = ''
        req = Request(environ)
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        containers = req.headers.get('container','')
        
        c_len = len(containers)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        
        resheaders = []
        for i in xrange(c_len):
            c_name = containers[i].encode("UTF-8")
            kwargs = {'m_name':c_name,'m_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = DataLogic().get_by_kwargs(**kwargs)
            if len(containers_get) == 0:
                try:
                    token = req.headers['token']
                    url = req.headers['auth_url']
                    container_name_construct = self.userName+'_'+str(parent_id)+'_'+c_name+'_'+self.domain+'_'+'container_'+"".join(re.split('\W+', str(datetime.datetime.now())))
                    container_storagename = hashlib.md5(container_name_construct).hexdigest()  
                    dic = {"storage_url":url, 'token':token, 'container':container_storagename,'headers':{}}
                    ApiMapping().scloud_put_container(**dic)
                    kwargs = {
                                'm_name' : c_name,
                                'm_storage_name' : container_storagename,
                                'm_domain_name' : self.domain,
                                'm_content_type' : 'container',
                                'm_status' : '1',   #'1' means available, '0' means not available
                                'm_uri' : container_storagename,
                                'm_hash' : '', #here we do not assign a hash name to the container
                                'm_size' : '/',
                                'm_parent_id' : parent_id,
                                'created' : str(datetime.datetime.now()),
                    }      
                    DataLogic().add_data(**kwargs);
                    for item in kwargs.items():
                        resheaders.append(item)
                        
                    start_response(HTTPCreated, resheaders)
                    return self.content
                    
                except Exception,e:
                    Log().error('PUT_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                    start_response(HTTPInternalServerError, resheaders)
                    return ''
            else:
                parent_id = containers_get[0].id
        start_response(HTTPConflict, resheaders)
        #return '403 Containers already exists\n'
        return ''
        
    def DELETE(self, environ,start_response):
        '''
            we propose that if the container is not empty, the delete operation
            is forbidden
        '''
        self.content = ''
        req = Request(environ)
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        containers = req.headers.get('container','')
        c_len = len(containers)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''
        resheaders = []
        for i in xrange(c_len):
            c_name = containers[i].encode("UTF-8")
            kwargs = {'m_name':c_name,'m_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = DataLogic().get_by_kwargs(**kwargs)
            
            if len(containers_get) != 0:
                parent_id = containers_get[0].id
                storage_name = containers_get[0].m_storage_name
                if i == c_len-1:
                    try:
#                         token = req.headers['token']
#                         url = req.headers['auth_url']                        
#                         dic = {"storage_url":url, 'token':token, 'container':storage_name,'headers':{}}
#                         ApiMapping().scloud_delete_container(**dic)
                        kwargs = {'id' : parent_id}
                        DataLogic().delete_data_by_id(**kwargs)
                        start_response(HTTPOk, resheaders)
                        return self.content                        
                    except Exception,e:
                        Log().error('DELETE_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                        start_response(HTTPInternalServerError, resheaders)
                        return self.content                        
            else:
                Log().error('Containers not Found, DELETE_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container']))
                start_response(HTTPNotFound, resheaders)
                return self.content                                  
        
    def POST(self, environ,start_response):
        
        '''POST can be used to change container metadata
        rename operation
        '''
        self.content = ''
        req = Request(environ)
        self.userName = req.headers.get('X-Auth-User', '')
        self.userKey = req.headers.get('X-Auth-Key', '')
        self.domain = req.headers.get('domain', '')
        containers = req.headers.get('container','')
        self.original_name = containers[-1]
        self.current_name = req.headers.get('current-name','')
        
        c_len = len(containers)# the length of the container
        root_id = Utils.getRootContainerId(self.domain)
        parent_id = root_id
        if parent_id == '':
            Log().error('can not get the domain ['+self.domain+"] id")
            start_response(HTTPNotFound,[("Content-type", "text/plain"),])
            return ''        
           
        resheaders = []
        if not self.original_name.strip() or not self.current_name.strip():
            start_response(HTTPBadRequest,[("Content-type", "text/plain"),])
            return self.content
        for i in xrange(c_len):
            c_name = containers[i].encode("UTF-8")
            
            # get all the containers corresponding to such conditions    
            kwargs = {'m_name':c_name,'m_parent_id':parent_id, 'm_content_type':'container'}
            containers_get = DataLogic().get_by_kwargs(**kwargs)
            
            if len(containers_get) != 0:
                if i!= c_len-1:
                    parent_id = containers_get[0].id
                else:
                    try:
                        kws = {'m_name':self.current_name,'m_parent_id':parent_id, 'm_content_type':'container'}
                        container_existing = DataLogic().get_by_kwargs(**kws) 
                        if (len(container_existing) != 0):
                            Log().error('same folder name existed, UPDATE_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container']))
                            start_response(HTTPConflict, resheaders)
                            #return 'same folder name existed\n'
                            return ''
                        parent_id = containers_get[0].id
                        kwargs = {'id':parent_id, 'm_name':self.current_name}
                        DataLogic().update_data_by_id(**kwargs)
                        start_response(HTTPOk, resheaders)
                        return self.content
                    except Exception,e:
                        Log().error('UPDATE_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container'])+' '+str(e))
                        start_response(HTTPInternalServerError, resheaders)
                        return self.content 
            else:
                Log().error('Containers not Found, POST_CONTAINER by '+req.headers.get('X-Auth-User')+': '+req.headers['domain']+'/'+str(req.headers['container']))
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
        return ContainerController(global_conf)
    
    
    
    