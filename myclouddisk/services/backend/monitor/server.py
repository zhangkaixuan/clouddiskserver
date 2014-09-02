# -*- coding: utf-8 -*-
'''
Created on 2013年9月11日

@author: adrian
'''
'''
Created on 2011-6-12
'''
import os
import webob
from webob import Request
from webob import Response
from paste.deploy import loadapp

from eventlet import wsgi
import eventlet

from services_config import services_available

# from services import services

class Server():
    '''
    目前支持的几大对象：
    domain, container, object, capability
    ---------
    domain: 逻辑域，用户权限管理单元，孩子节点为container
    container: 文件夹， 孩子节点为container 和 object【底层云存储实现应该是flat结构，这里做了扩展】 
    object：文件， 最终存储在文件系统上
    capability： 功能对象， 标明domain， container， object几大对象针对当前用户开放的功能
    ----------
    
    具体操作：
        0.查看 domain[public, protected, private]
        1.创建、查看、罗列、删除 container
        2.修改、获取container的访问权限[public_read, public_read_write, private]
        3.上传、查看、罗列、删除 Object
        4.查看 capability
        
        ----------not finished yet
        5.对于大文件支持分片上传(Multi-Part Upload)
        6.访问时支持If-Modified-Since和If-Match等HTTP参数
    
    
    公共请求头（5个）：
        Content-Type, host, X-CDMI-Specification-Version, Authorization, date
        通过如下代码获得：
        self.content_type = req.headers.get('Content-Type', '')
        self.host = req.headers.get('host', '')
        self.cdmi_version = req.headers.get('X-CDMI-Specification-Version', '')
        self.authorization = req.headers.get('Authorization', '')
        self.date = req.headers.get('date', '')
    公共响应体(8个):
        objectType, objectID, objectName, parentURI, parentID, domainURI, capabilitiesURI, metadata
    
    例子：
    Api Url Pattern:
        Domain:
            PUT: http://[localhost:8080]/scloud_domain/MyDomain HTTP/1.1
                [header]
                Host: scloud.ecust.com
                Accept: application/scloud-domain
                Content-Type: application/scloud-domain-public[private, protected]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            GET: http://[localhost:8080]/scloud_domain/MyDomain HTTP/1.1
                [header]
                Host: scloud.ecust.com
                Accept: application/scloud-domain
                Content-Type: application/scloud-domain-public[private, protected]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            DELETE: http://[localhost:8080]/scloud_domain/MyDomain HTTP/1.1
                [header]
                Host: scloud.ecust.com
                Accept: application/scloud-domain
                Content-Type: application/scloud-domain-public[private, protected]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            HEAD: http://[localhost:8080]/scloud_domain/MyDomain HTTP/1.1
                [header]
                Host: scloud.ecust.com
                Accept: application/scloud-domain
                Content-Type: application/scloud-domain-public[private, protected]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
        
        Container:
            PUT: http://[localhost:8080]/[container]/[the-container]/ HTTP/1.1
                [params]
                :param container: could be an existing container or zero or many
                :param the-contianer: the container u want to create
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-container-pr[prw, pri]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            DELETE: http://[localhost:8080]/[container]/[the-container]/ HTTP/1.1
                [params]
                :param container: could be an existing container or zero or many
                :param the-contianer: the container u want to delete
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-container-pr[prw, pri]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            GET: http://[localhost:8080]/[container]/[the-container]/ HTTP/1.1
                [params]
                :param container: could be an existing container or zero or many
                :param the-contianer: the container u want to get
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-container-pr[prw, pri]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            HEAD: http://[localhost:8080]/[container]/[the-container]/ HTTP/1.1
                [params]
                :param container: could be an existing container or zero or many
                :param the-contianer: the container u want to head
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-container-pr[prw, pri]
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            POST: http://[localhost:8080]/[container]/[the-container]/ HTTP/1.1
                [params]
                :param container: could be an existing container or zero
                :param the-contianer: the container u want to change the container name
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-container-pr[prw, pri]
                X-CDMI-Specification-Version: 1.0.2
                X-Current-Name: current-name
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
        Object:
            PUT: http://[localhost:8080]/[container]/[MyObject] HTTP/1.1
                [params]
                :param container: could be an existing container or many
                :param MyObject: the object u want to create
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-object
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
                [request body]
                {
                   "mimetype" : "text/plain",
                   "metadata" : { },
                   "valuetransferencoding" : "base64"
                   "value" : "VGhpcyBpcyB0aGUgVmFsdWUgb2YgdGhpcyBEYXRhIE9iamVjdA=="
                }
            GET: http://[localhost:8080]/[container]/[MyObject] HTTP/1.1
                [params]
                :param container: could be an existing container or many
                :param MyObject: the object u want to get
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-object
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            DELETE: http://[localhost:8080]/[container]/[MyObject] HTTP/1.1
                [params]
                :param container: could be an existing container or many
                :param MyObject: the object u want to delete
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-object
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
            POST: http://[localhost:8080]/[container]/[MyObject] HTTP/1.1
                [params]
                :param container: could be an existing container or many
                :param MyObject: the object u want to create
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-object
                X-CDMI-Specification-Version: 1.0.2
                X-Current-Name: current-name
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
                
            HEAD: http://[localhost:8080]/[container]/[MyObject] HTTP/1.1
                [params]
                :param container: could be an existing container or many
                :param MyObject: the object u want to create
                [header]
                Host: domain.scloud.ecust.com
                Accept: application/scloud-container
                Content-Type: application/scloud-object
                X-CDMI-Specification-Version: 1.0.2
                Date: Fri, 24 Feb 2012 07:18:48 GMT
                Authorization: scloud x-user-name: x-user-key
        
    
    '''
    def __init__(self):
        pass
    def start(self):
        
        configfile="config.ini"
        appname="pdl"
        wsgi_app = loadapp("config:%s" % os.path.abspath(configfile), appname)
        wsgi.server(eventlet.listen(('localhost', 8080)), wsgi_app)
    def stop(self):    
        pass
    
    def restart(self):
        self.stop()
        self.start()


if __name__ == '__main__':
    scloud_server = Server()
    #启动wsgi服务器
    scloud_server.start()



