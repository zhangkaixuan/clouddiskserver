# -*- coding: utf-8 -*-
'''
Created on 2013年12月2日

@author: adrian
'''

import pika
import sys
import json
import httplib, urllib

def url_go(domain_id, size, opr):
    #:param opr is GET or POST
    #:param domain_id is the id of domain
    #:param size is size of object file
    
    body = ''

    conn = httplib.HTTPConnection("localhost:8888")
    conn.request(opr, '/?id='+domain_id+'&size='+size, body, {})
    try:
        response = conn.getresponse()
        status = response.read()
        return status
    except Exception, e:
        print e

if __name__ == '__main__':
    print url_go('2', '111111111', 'GET')