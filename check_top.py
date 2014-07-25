#/usr/bin/python
#coding=utf-8

'''
auth:wuqichao@playcrab.com
date:2014-06-17 12:00

'''
import time
from pprint import pprint
from assets import assets
from custom.db.mysql import Custom_MySQL
from manage.mtask import Mtask
from manage.auto_run import auto_run

            
        
class last_ip(auto_run):
    
    
    def __init__(self):
        
        temp = []
        for i in assets.get_assets():
            i['cmd']  = '''/usr/bin/top -bn 1|grep Cpu| awk '{print $5}' | cut -f 1 -d "."'''
            temp.append(i)
            
        super(last_ip, self).__init__(temp)
        
    def call_back(self,data=[]):
        
      
        for result in data:
            print result
            continue
            
                

if __name__ == '__main__':
    a =last_ip().start()