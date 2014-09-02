

import pika
import sys
import json
sys.path.append('/Users/adrian/Dropbox/workspace/EcustCloudStorage')


from services.backend.log.log import Log
'''codes added to run in command'''
# for mac

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'


def callback(ch, method, properties, body):
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
 
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
 
channel.start_consuming()