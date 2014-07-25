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
        for i in assets.get_assets():
            i['cmd']  = '''last -n 10 | awk '{print $3}'|grep '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' '''
            temp.append(i)
            
        super(last_ip, self).__init__(temp)
        
    def call_back(self,data=[]):
        
        
        db = Custom_MySQL(using='log')
        
        sql = "insert into last_ip (id,ip,login_ip) values(null,%s,%s)"
        
        for result in data:
            
            if int(result['flag']) == 1:
     
                ips = json.loads(result['data'])
                host = result['ip']
    
                set_param =[]
                for ip in ips:
                    set_param.append(tuple([host,ip]))
                db.executemany(sql,set_param)
                db.commit()
            else:
                print result
        
                

if __name__ == '__main__':
    a =last_ip().start()