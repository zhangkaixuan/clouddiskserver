# -*- coding: utf-8 -*-
# Copyright (c) 2010-2012 OpenStack, LLC.

# how to use the apiMapping
# 1. get the params list from the config file
# 2. construct a dictionary according to the param list
# 3. diliver the dict as **param to the standard function

'''
Created on 2013年10月15日

@author: adrian
'''


from xml.dom import minidom

from api.settings import AUTH_URL
from api.swift import swiftAPI
from api.s3 import s3API
from api.keystone import client

from proxy.params import *

class ApiMapping():            
    """
    SCloud api mapping Class by Adrian
    NOTE:
        !important
        the params listed in config standard fun should include all the params which will be refered by swift ,s3 or other
        api system
    """
    def __init__(self):
        '''
            we here do not init things in order to make the functions in swift or s3 can work totally depends on 
            the apiconfig.xml file
        '''
        
        pass
            
            
    def _api_mapping(self, fun_name, api_type, **kws):
#         apis = minidom.parse('/Users/adrian/Dropbox/workspace/EcustCloudStorage/api/apiconfig.xml')
        apis = minidom.parse(APIConfigFile)
        
        for api in apis.getElementsByTagName('api'):
            if api.attributes['name'].firstChild.nodeValue == fun_name:
                
                swift_api_name = api.getElementsByTagName(api_type)[0].getElementsByTagName('name')[0].firstChild.nodeValue
                param_dict = {}
                
                params = api.getElementsByTagName(api_type)[0].getElementsByTagName('input')[0] \
                            .getElementsByTagName('param')
                for param in params:
                    key = param.attributes['name'].firstChild.nodeValue
                    value = kws[param.attributes['ref'].firstChild.nodeValue]
                    param_dict[key] = value
                    
                return getattr(swiftAPI, swift_api_name)(**param_dict)
                break
    
    def scloud_get_auth(self,**kws):
        """Wrapper for :func:`head_account`"""
        return self._api_mapping('scloud_get_auth','swift',**kws)
    
    def scloud_head_domain(self,**kws):
        """Wrapper for :func:`head_account`"""
        return self._api_mapping('scloud_head_domain','swift',**kws)

    def scloud_get_domain(self, **kws):
#         marker=None, limit=None, prefix=None,full_listing=False
        return self._api_mapping('scloud_get_domain','swift',**kws)
        """Wrapper for :func:`get_account`"""

    def scloud_post_domain(self, **kws):
#         headers
        """Wrapper for :func:`post_account`"""
        return self._api_mapping('scloud_post_domain','swift',**kws)

    def scloud_head_container(self, **kws):
#         container
        """Wrapper for :func:`head_container`"""
        return self._api_mapping('scloud_head_container','swift',**kws)

    def scloud_get_container(self, **kws):
#         container, marker=None, limit=None, prefix=None,delimiter=None, full_listing=False
        """Wrapper for :func:`get_container`"""
        return self._api_mapping('scloud_get_container','swift',**kws)

    def scloud_put_container(self, **kws):
#         container, headers=None
        """Wrapper for :func:`put_container`"""
        return self._api_mapping('scloud_put_container','swift',**kws)

    def scloud_post_container(self, **kws):
#         container, headers
        """Wrapper for :func:`post_container`"""
        return self._api_mapping('scloud_post_container','swift',**kws)

    def scloud_delete_container(self, **kws):
#         container
        """Wrapper for :func:`delete_container`"""
        return self._api_mapping('scloud_delete_container','swift',**kws)

    def scloud_head_object(self, **kws):
#         container, obj
        """Wrapper for :func:`head_object`"""
        return self._api_mapping('scloud_head_object','swift',**kws)

    def scloud_get_object(self, **kws):
#         container, obj, resp_chunk_size=None
        """Wrapper for :func:`get_object`"""
        return self._api_mapping('scloud_get_object','swift',**kws)

    def scloud_put_object(self, **kws):
#         container, obj, contents, content_length=None,etag=None, chunk_size=65536, content_type=None,headers=None
        return self._api_mapping('scloud_put_object','swift',**kws)

    def scloud_post_object(self, **kws):
#         container, obj, headers
        return self._api_mapping('scloud_post_object','swift',**kws)

    def scloud_delete_object(self, **kws):
#         container, obj
        return self._api_mapping('scloud_delete_object','swift',**kws)

def test():
    dic = {"auth_url":AUTH_URL, 'user':'20141001', 'key':'123456', 'domain_name':'20141001'}
    url, token = ApiMapping().scloud_get_auth(**dic)
    
    #print ApiMapping().scloud_get_container(**dic)
    
    print url, token
    
#     file = open('/Users/adrian/Desktop/scloud.sql')
#     dic = {"storage_url":url, 'token':token, 'container':'5','headers':{'hello':'df'}, \
#            'object':'1234ddd6.sql','contents':file}
#     result = ApiMapping().scloud_get_domain(**dic)
    #dic = {"storage_url":url, 'token':token}
    #result = ApiMapping().scloud_get_domain(**dic)
    #print result
    
    
if __name__ == "__main__":
    test()
    
    
    