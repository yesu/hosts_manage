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
            i['cmd']  = """df -B 1M | grep '/dev' | awk '{print $2" "$3}'|awk 'BEGIN{s1=0;s2=0}{s1+=$1;s2+=$2}END{printf "%.2f",(s2/s1)*100}'"""
            temp.append(i)
            
        super(df_used, self).__init__(temp)
        
    def call_back(self,data=[]):
        
        db = Custom_MySQL(using='log')   
        last_insert_id =  db.insert('df_batch',**{})
        db.commit()
        
        sql = "insert into df_detail (id,ip,df_used) values(null,%s,%s)"
        
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
