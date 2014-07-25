#/usr/bin/python
#coding=utf-8

'''
auth:wuqichao@playcrab.com
date:2014-06-17 12:00

'''

import json
from custom.request.p import get
from custom.db.mysql import Custom_MySQL
db = Custom_MySQL(using='remote_manage')

class ip2name(object):
    
    def __init__(self):
        
        self.out_ip = ['106.37.232.112',
                       '106.37.232.113',
                       '106.37.232.114',
                       '106.37.232.115',
                       '106.37.232.116',
                       '106.37.232.117',
                       '106.37.232.118',
                       '106.37.232.119'
                       ]
    
    def get_ip(self):
        
        param = "'"+"','".join(self.out_ip)+"'"
          
        return db.query("SELECT DISTINCT(`last_ip`.`login_ip`) as ip from remote_manage.last_ip \
                where login_ip \
                not in \
                (SELECT public_ip from center_app.assets where public_ip !='')\
                and login_ip NOT like '10.%%' \
                and login_ip not in (%s) " ,param)
        
    def run(self):
        
        data = self.get_ip()
        print '不明ip共计:%s'%len(data)
        for host in data:
             urls ='http://ip.taobao.com/service/getIpInfo.php?ip=%s'%host['ip']
             n = json.loads(get(urls))
             
             if n['code'] == 0:
                 print n['data']['ip'],n['data']['country'],n['data']['region'],n['data']['city'],n['data']['area'],n['data']['isp']
             
               
    def __del__(self):
        pass
    
    
if __name__ == '__main__':
    
    n = ip2name()
    n.run()
    




