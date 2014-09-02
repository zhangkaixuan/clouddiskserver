# -*- coding: utf-8 -*-
'''
Created on 2013年10月28日

@author: adrian
'''
import pika
import sys
import json
import httplib, urllib

'''codes added to run in command'''
# to add the sys path in order python command in terminal can work 
# for mac
sys.path.append('/Users/adrian/Dropbox/workspace/EcustCloudStorage')
#for windows
# sys.path.append('C:\Users\jipingzh\Dropbox\workspace\EcustCloudStorage')


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='pie_queue')


def url_go(domain_id, size, opr):
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
 
def on_request(ch, method, props, body):
    
    mes_dic = json.loads(body)
    #获得操作指令   GET or POST
    opr = mes_dic.pop('opr')
    #获得文件大小
    size = mes_dic.pop('size')
    #获得域id
    domain_id = mes_dic.pop('id')
     
     
    response = url_go(domain_id, size, opr)
         
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)
 
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='pie_queue')
 
print " [x] Awaiting RPC requests"
channel.start_consuming()




