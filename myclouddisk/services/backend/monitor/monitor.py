'''
Created on 2013-11-19

@author: Administrator
'''
from urllib2 import urlopen
from socket import socket
from sys import argv
from services.backend.log.log import Log 
def tcp_test(server_info):
    cpos = server_info.find(':')
    try:
        sock = socket()
        sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
        sock.close
        return True
    except:
        return False
 
def http_test(server_info):
    try:
        data = urlopen(server_info).read()
        return True
    except:
        return False
 
def server_test(test_type, server_info):
    if test_type.lower() == 'tcp':
        return tcp_test(server_info)
    elif test_type.lower() == 'http':
        return http_test(server_info)
 
if __name__ == '__main__':
#   if len(argv)!=3:
#       print "wrong num of arguments."
#   elif not server_test(argv[1],argv[2]):
#        print"unable to connect to service %s %s."%(argv[1],argv[2])
       print   server_test("http","http://127.0.0.1:8000")    
       print   server_test("http","http://127.0.0.1:8080")       
       Log().error("wocuole")       
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
