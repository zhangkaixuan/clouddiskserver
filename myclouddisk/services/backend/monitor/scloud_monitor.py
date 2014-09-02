# -*- coding: utf-8 -*-
'''
Created on 2013年11月4日

@author: adrian


'''
from api import api_map

scloud_api = api_map.ApiMapping()

from api.settings import AUTH_URL
from services.frontend.resmgr.meta_client import  MetaClient
import json


def test():
    dic = {"auth_url":AUTH_URL, 'user':'admin', 'key':'ADMIN', 'domain_name':'admin'}
    url, token = scloud_api.scloud_get_auth(**dic)
    
#     file = open('/Users/adrian/Desktop/scloud.sql') 
    dic = {"storage_url":url, 'token':token, 'container':'5','headers':{'hello':'df'}, \
           'object':'1234ddd6.sql'}
    containers = scloud_api.scloud_get_domain(**dic)[1]
    for c in containers:
        print c.get('name')
        kwargs = {'m_storage_name':c.get('name'), 'metadata_opr':'get'}
        containers_get = MetaClient().call(**kwargs)
        containers_dic = json.loads(containers_get)
        
            
        if len(containers_dic) == 0 and c.get('count')==0:
            dic = {"storage_url":url, 'token':token, 'container': c.get('name'),'headers':{'hello':'df'}}
#             delete the storage source
            scloud_api.scloud_delete_container(**dic)
#             delete the metadata
#             MetaClient().call(**{'id':id, 'metadata_opr':'delete'})
        
def find_all_containers():            
    dic = {"auth_url":AUTH_URL, 'user':'admin', 'key':'ADMIN', 'domain_name':'admin'}
    url, token = scloud_api.scloud_get_auth(**dic)
    
    file = open('/Users/adrian/Desktop/scloud.sql')
    dic = {"storage_url":url, 'token':token, 'container':'5','headers':{'hello':'df'}, \
           'object':'1234ddd6.sql','contents':file}
    containers = scloud_api.scloud_get_domain(**dic)[1]
    for c in containers:
        print c
    
    
    
if __name__ == "__main__":
    test()
#     find_all_containers()