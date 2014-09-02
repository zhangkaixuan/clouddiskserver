# -*- coding: utf-8 -*-
'''
Created on 2013年9月11日

@author: adrian
'''
import os
import webob
from webob import Request
from webob import Response
from paste.deploy import loadapp

from eventlet import wsgi
import eventlet

from proxy.params import *

# from services import services

class Server():
    '''
    @important
    the server listen on port :8888
    server port can be changed if any conflict occurs
    ---------------------------    

    Pie Server
    用来对用户域流量进行统计和计算
    用来监控用户的网络流量
    
    Pie服务 模块主要为付费统计服务进行服务
    '''
    def __init__(self):
        pass
    def start(self):
        
        configfile = pie_server_config_file 
        appname="pie"
        wsgi_app = loadapp("config:%s" % os.path.abspath(configfile), appname)
        wsgi.server(eventlet.listen(('localhost', 8888)), wsgi_app)
    def stop(self):    
        pass
    
    def restart(self):
        self.stop()
        self.start()


if __name__ == '__main__':
    scloud_server = Server()
    #启动wsgi服务器
    scloud_server.start()



