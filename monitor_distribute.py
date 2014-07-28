#/usr/bin/python
#coding=utf-8

'''
auth:wuqichao@playcrab.com
date:2014-06-17 12:00

'''
import json
import time
from pprint import pprint
from assets import assets
from custom.db.mysql import Custom_MySQL
from manage.mtask import Mtask
from manage.auto_run import auto_run

            
        
class last_ip(auto_run):
    
    
    def __init__(self):
        
        temp = []
        for i in assets.get_monitor():
            i['cmd']  = '''nohup wget --no-check-certificate https://raw.githubusercontent.com/djshell/hosts_manage/master/monitor/client.py -O client.py;python client.py &'''
            temp.append(i)
            
        super(last_ip, self).__init__(temp)
        
    def call_back(self,data=[]):
        
        print data
        
                

if __name__ == '__main__':
    a =last_ip().start()