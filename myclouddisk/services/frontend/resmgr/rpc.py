# -*- coding: utf-8 -*-
'''
Created on 2013年11月4日

@author: adrian
'''
import pika
import uuid
import json



class Rpc(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

    def _on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            
    def _start_cast_consume(self, exchange):
        
        channel = self.connection.channel()
        channel.exchange_declare(exchange='logs',
                                 type='fanout')
        
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        
        channel.queue_bind(exchange=exchange,
                           queue=queue_name)
        
        print ' [*] Waiting for logs. To exit press CTRL+C'
        
        def callback(ch, method, properties, body):
            print " [x] %r %s" % (body,queue_name)
        
        channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def call(self, routing_key, **meg):
        
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self._on_response, no_ack=True,
                                   queue=self.callback_queue)
        self.response = None
        meta_json = json.dumps(meg, ensure_ascii=False)

        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key = routing_key,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=meta_json)
        while self.response is None:
            self.connection.process_data_events()
            
        return self.response
    
    def cast(self, exchange, message):
        
        channel = self.connection.channel()
        
        channel.exchange_declare(exchange=exchange,
                                 type='fanout')
        channel.basic_publish(exchange=exchange,
                              routing_key='',
                              body=message)
        print " [x] Sent %r" % (message,)
        
#         self._start_cast_consume(exchange)
        self.connection.close()

# For Testing
if __name__ == '__main__':
    rpc = Rpc()
    
    dic = {"id":"2", "size":"11111111", "opr": 'GET'}
    print rpc.call('pie_queue', **dic)
