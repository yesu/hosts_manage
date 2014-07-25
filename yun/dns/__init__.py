#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-16 11:35:57
usege:

"""

import os
import json
import time
import urllib
import urllib2
from custom.config.ini import DictConfigParser
from custom.request import ajax
ini_path = os.path.join(os.path.abspath('./config/'),'yun_config')
ini_section_key  ='dnspod'


class dns(object):
    

    
    def _rebot(self):
       
        n = DictConfigParser(ini_path)
        user = n[ini_section_key]['id'].encode('utf-8')
        passwd = n[ini_section_key]['key'].encode('utf-8')

    
        data = {'login_email':user,
                'login_password':passwd,
                'format':'json',
                'domain_id':'2191590'
               }
        json_data = ajax('https://dnsapi.cn/Record.List',data)
         
        domain = {}
        
        for s in json_data['records']:
            na = s['name']+'.playcrab.com'
            va = s['value']
            if s['type'] == 'A':
                domain[na] = va
        return domain
     
        
    def get_result(self):
       
        return self._rebot()
        
