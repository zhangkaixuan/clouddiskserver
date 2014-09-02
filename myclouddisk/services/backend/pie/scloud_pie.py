# -*- coding: utf-8 -*-
'''
Created on 2013年11月30日

@author: adrian
'''
from services.frontend.resmgr.rpc import Rpc
import json
import os
import webob
from webob import Request
from webob import Response

from proxy.params import *

class Pie(object):
    '''
    Pie Service to statistics data on the domain usage or the bandwidth consumption
    Pie 服务用来统计用户域空间使用请情况和带宽流量
    '''
    def __init__(self, global_conf):
        #value requrired
        self.global_conf = global_conf

    def scloud_pie(self, environ, start_response, domain_id, size):
        '''
        改变用户存储空间的大小。
        用于对用户存储空间进行容量统计
        '''
        #Initialize Rpc instance
        self.rpc = Rpc()
        
        domain_id = int(domain_id)
        size = float(size)
        #get current size of domain size
        kwargs = {'metadata_target':'domain', 'id':domain_id, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        #default domain size is 2G
        domain_size = float(domains_dic[0].get('size', '').strip('G'))
        domain_left_size = float(domains_dic[0].get('left', '').strip('G'))
        #Compute the current domain size
        domain_size_k = domain_size*1024*1024
        domain_left_size_k = domain_left_size*1024*1024
        
        #size default bytes
        size_k =size/1024.0
        current_size_k = domain_size_k + size_k+0.0
        current_left_size_k = domain_left_size_k - size_k +0.0
        
        current_size_G = current_size_k/1024.0/1024.0
        current_left_size_G = current_left_size_k/1024.0/1024.0
        
        
        #Update domain by id
        kwargs = {'metadata_target':'domain', 'id':domain_id, 'left':str(current_left_size_G)+'G', 'size':str(current_size_G)+'G', 'metadata_opr':'update'}
        self.rpc.call('meta_queue', **kwargs)
        
        
    
    def scloud_pie_status_check(self, environ, start_response, domain_id, size):
        '''
        如果文件大小<域现存的空间：
            return 1 #表示能够存放该文件
        else：
            return 0 #表示空间大小不足，不能够用来存储文件
        '''
        #Initialize Rpc instance
        self.rpc = Rpc()
        domain_id = int(domain_id)
        size = float(size)
        
        #get current size of domain size
        kwargs = {'metadata_target':'domain', 'id':domain_id, 'metadata_opr':'get'}
        domains_get = self.rpc.call('meta_queue', **kwargs)
        domains_dic = json.loads(domains_get)
        #default domain size is 2G
        domain_left_size = float(domains_dic[0].get('left', '').strip('G'))
        domain_left_size_k = domain_left_size*1024*1024
        
        object_size_k = size/1024.0
        
        #判断现存的domain 大小是否允许存放该文件
        if object_size_k > domain_left_size_k: return 0
        return 1
        
    
    def __call__(self,environ,start_response):
        req = Request(environ)
        rpc = Rpc()

        print req
        
        print req.params
        domain_id = req.params.get('id', '')
        size = (req.params.get('size', ''))
        self.content = ''
        
        print "the domain_id is %s, and size is %s" % (domain_id, size)
        
        if domain_id == '' or size == '':
            log_dic = {"log_flag":"error", "content":'scloud pie service can not get domain_id param or size param, please check the url'}
            rpc.cast('logs', json.dumps(log_dic))
            start_response(HTTPBadRequest, [])
            
        if req.method == 'GET':
            #使用如下方式进行curl参数请求
            #curl -i http://localhost:8888 -d "id=2" -d "size=1111111111111"  -G
            #content-length 可以根据返回内容自动进行计算
            
            self.content = str(self.scloud_pie_status_check(environ, start_response, domain_id, size))
            start_response('200 OK', [])

        if req.method == "POST":
            self.scloud_pie(environ, start_response, domain_id, size)
            start_response(HTTPOk, [])
            
        return [self.content]
        
    @classmethod
    def factory(cls,global_conf,**kwargs):
        print "in ShowVersion.factory", global_conf, kwargs
        return Pie(global_conf)
        

        