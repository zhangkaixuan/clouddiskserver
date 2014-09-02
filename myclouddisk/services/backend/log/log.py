# -*- coding: utf-8 -*-
'''
Created on 2013年10月15日

@author: adrian
'''
import logging
import os
from proxy.params import LogFilePath

class Log:
    def __init__(self):
#         if not os.path.isfile(os.path.join(os.getcwd(), 'log.txt')):
        logging.basicConfig(filename = LogFilePath, \
                            level = logging.INFO, format = '[%(asctime)s] - [%(levelname)s]: [%(message)s]')
    
    def _format(self,meg):
        return " ".join(meg.split())
    
    def debug(self, meg):
        meg = self._format(meg)
        logging.debug(meg)
        
    def info(self, meg):
        meg = self._format(meg)
        logging.info(meg)
        
    def warning(self, meg):
        meg = self._format(meg)
        logging.warning(meg)
        
    def error(self, meg):
        meg = self._format(meg)
        logging.error(meg)
        
    
