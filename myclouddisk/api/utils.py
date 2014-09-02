# -*- coding: utf-8 -*-
'''
Created on 2014年8月19日

@author: adrian
'''

from metadata.data_model import DataLogic
from services.backend.log.log import Log
class Utils(object):
    def __init__(self):
        """Do nothing, by default."""
       
    @staticmethod 
    def getRootContainerId(domainName):
        kws = {'m_name':'root_container', 'm_tenant_name':domainName, 'm_content_type':'container'}
        root_id = ''
        try:
            root_id = DataLogic().get_by_kwargs(**kws)[0].id
        except Exception, e:
            Log().error('工具类getRootContainerId方法异常，domainName = '+domainName+str(e))
        return root_id
    
    @staticmethod 
    def getRootContainerStorageName(domainName):
        kws = {'m_name':'root_container', 'm_tenant_name':domainName, 'm_content_type':'container'}
        storage_name = ''
        try:
            storage_name = DataLogic().get_by_kwargs(**kws)[0].m_storage_name
        except Exception, e:
            Log().error('工具类getRootContainerStorageName方法异常，domainName = '+domainName+str(e))
        return storage_name


if __name__=="__main__":
    print  Utils.getRootContainerStorageName('xxxxxx')