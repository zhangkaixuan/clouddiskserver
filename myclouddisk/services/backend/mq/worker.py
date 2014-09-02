# -*- coding: utf-8 -*-
'''
Created on 2013年12月3日

@author: adrian
'''
import pika
import sys
import json
import httplib, urllib
from xml.dom import minidom
#For command running

from metadata.data_model import DataLogic
from metadata.domain_model import DomainLogic
from services.backend.log.log import Log
from proxy.params import *

from services.backend.exception import scloud_exception
from  eventlet.greenpool import GreenPool



class Worker(object):
    '''
    用户注册的service，在xml配置完成之后，要在此实现相应的on_request方法
    '''
    def __init__(self):
        pass
    
    
#     def start(self, host, exchange, exchange_type, routing_key, on_request_name):
    def start(self, **params):
        '''
        :param host: 用户配置的Rabbit Mq Server所在IP地址
        :param exchange: 用户配置的交换机名称
        :param exchange_type: 用户配置的交换机类型
        :param routing_key: 用户配置的路由key， 此key等同于queue的名称
        :param on_request_name: 用户配置的服务器接收响应的方法名称
        '''
        host = params.get('host')
        exchange = params.get('exchange')
        service_type = params.get('service_type')
        routing_key = params.get('routing_key')
        on_request_name = params.get('on_request_name')
        
        
        
        
        
        if not (service_type and exchange and routing_key and on_request_name):
            raise scloud_exception.APIException()
        
        if service_type == 'call':
            connection = pika.BlockingConnection(pika.ConnectionParameters(host = host or 'localhost'))
            channel = connection.channel()
            channel.queue_declare(queue = routing_key)
            channel.basic_qos(prefetch_count = 1)
            
            #Getattr function here to get the Worker instance's function inside
            channel.basic_consume(getattr(self, on_request_name), queue = routing_key)
             
            print " [x] Awaiting RPC requests " + on_request_name
            channel.start_consuming()
        if service_type == 'cast':
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host or 'localhost'))
            channel = connection.channel()
            
            channel.exchange_declare(exchange=exchange,
                                     type='fanout')
            
            result = channel.queue_declare(exclusive=True)
            queue_name = result.method.queue
            
            channel.queue_bind(exchange='logs',
                               queue=queue_name)
 
            #Getattr function here to get the Worker instance's function inside
            channel.basic_consume(getattr(self, on_request_name),
                      queue=queue_name,
                      no_ack=True)
 
            print " [x] Awaiting RPC requests " + on_request_name
            channel.start_consuming()
        
    def url_go(self, domain_id, size, opr):
        #:param opr is GET or POST
        #:param domain_id is the id of domain
        #:param size is size of object file
    
        body = ''
    
        conn = httplib.HTTPConnection("localhost:8888")
        conn.request(opr, '/?id='+domain_id+'&size='+size, body, {})
        try:
            response = conn.getresponse()
            result = response.read()
            return result
        except Exception, e:
            print e
 
    def on_request_pie(self, ch, method, props, body):
        
        mes_dic = json.loads(body)
        #获得操作指令   GET or POST
        opr = mes_dic.pop('opr')
        #获得文件大小
        size = mes_dic.pop('size')
        #获得域id
        domain_id = mes_dic.pop('id')
         
         
        response = self.url_go(domain_id, size, opr)
             
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    def on_request_metadata(self, ch, method, props, body):
        response = ''
        mes_dic = json.loads(body)
        
        #获得元数据操作指令
        opr = mes_dic.pop('metadata_opr')
        #获得目标元数据
        target = mes_dic.pop('metadata_target')
    
        #操作 object或container的元数据
        if target == 'data':
            if 'add' == opr:
                response = DataLogic().add_data(**mes_dic)
            #     delete a data by id
            if 'delete' == opr:
                response = DataLogic().delete_data_by_id(**mes_dic)
            #     update data by id   
            if 'update' == opr:
                response = DataLogic().update_data_by_id(**mes_dic)
            #     get data by conditions
            if 'get' == opr:
                response = DataLogic().get_by_kwargs(**mes_dic)
                
        #操作domain的元数据
        if target == 'domain':
            if 'add' == opr:
                response = DomainLogic().add_data(**mes_dic)
            #     delete a data by id
            if 'delete' == opr:
                response = DomainLogic().delete_data_by_id(**mes_dic)
            #     update data by id   
            if 'update' == opr:
                response = DomainLogic().update_data_by_id(**mes_dic)
            #     get data by conditions
            if 'get' == opr:
                response = DomainLogic().get_by_kwargs(**mes_dic)
        
        print response
            
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def on_request_log(self, ch, method, properties, body):
        mes_dic = json.loads(body)
        
    #     print mes_dic
        flag = mes_dic.get('log_flag', '')
        content = mes_dic.get('content', '')
        
        print flag, content
        if 'info' == flag:
            Log().info(content)
        if 'debug' == flag:
            Log().debug(content)
        if 'warning' == flag:
            Log().warning(content)
        if 'error' == flag:
            Log().error(content)


def get_services():
    '''
    return a service list[s1,s2,s3]
    '''
    services_dict = {}
    services = minidom.parse(ServiceConfigFile)
    for service in services.getElementsByTagName('service'):

        service_name = service.getElementsByTagName('name')[0].firstChild.nodeValue
#         host='localhost', exchange='metadata', service_type='call', routing_key='meta_queue', on_request_name = 'on_request_metadata'
        service_params = {}
        service_params['service_type'] = service.attributes['type'].firstChild.nodeValue
        service_params['host'] = service.getElementsByTagName('host')[0].firstChild.nodeValue
        service_params['exchange'] = service.getElementsByTagName('params')[0].getElementsByTagName('exchange')[0].firstChild.nodeValue
        service_params['routing_key'] = service.getElementsByTagName('params')[0].getElementsByTagName('queue')[0].firstChild.nodeValue
        service_params['on_request_name'] = service.getElementsByTagName('params')[0].getElementsByTagName('callback')[0].firstChild.nodeValue
        
        services_dict[service_name] = service_params
        
    return services_dict


#For Test
if __name__ == '__main__':
    
    import threading
    pool = GreenPool()
    
    services = get_services()
    service = sys.argv[1]
    
    if service in services.keys():
        pool.spawn(Worker().start(**services.get(service, {})))
        
    else: print 'no such service'
        
