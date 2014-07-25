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
from manage.auto_run import auto_run
from custom.db.mysql import Custom_MySQL
            
        
class df_used(auto_run):
    
    
    def __init__(self):
        
        temp = []
        for i in assets.get_assets():
            i['cmd']  = """mpstat -P ALL  1 10 | grep all | awk '{print $11}' | awk 'BEGIN{sum=0;num=0}{sum+=$1;num+=1}END{print sum/num}'"""
            temp.append(i)
            
        super(df_used, self).__init__(temp)
        
    def call_back(self,data=[]):
            
        db = Custom_MySQL(using='log')   
        last_insert_id =  db.insert('cpu_batch',**{})
        db.commit()
        
        sql = "insert into cpu_detail (id,ip,cpu_used) values(null,%s,%s)"
        
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
    a =df_used().start()



