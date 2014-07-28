#/usr/bin/python
#coding=utf-8

'''
auth:wuqichao@playcrab.com
date:2014-06-17 12:00

'''

from pprint import pprint
from custom.db.mysql import Custom_MySQL


        
class assets(object):
    '''
    所有机器信息
    '''
    def __init__(self):
        pass
    
    @staticmethod
    def get_assets():
        n = Custom_MySQL(using='center_app')
        
        return n.query('select public_ip as ip,22 as port,"playcrab" as  user,pwd  \
                        from assets \
                        where \
                        public_ip !="" and public_ip !="NULL" \
                        and public_ip not in("115.29.12.230","115.29.12.219","49.213.111.2","49.213.111.3","49.213.111.4","49.213.111.5","49.213.111.6") \
                        order by id')
        
    @staticmethod
    def get_monitor():
        n = Custom_MySQL(using='center_app')
        
        return n.query('select public_ip as ip,22 as port,"playcrab" as  user,pwd  \
                        from assets \
                        where \
                        public_ip ="115.29.10.48" \
                       ')
                
    @staticmethod    
    def get_idcs(idc_name):
        db = Custom_MySQL(using='center_app')
        sql ="select id as idc_id,prefix  from idc where name like  %s and is_del = 0" 
        p=(idc_name+'%',)
        return db.query(sql,*p)
    
    @staticmethod
    def get_ali_idcs():

        return assets.get_idcs('ali-yun')
    
    @staticmethod
    def get_ucloud_idcs():
        return assets.get_idcs('ucloud')
    
        
    @staticmethod
    def get_amazon_idcs():
        return assets.get_idcs('amazon')        
          
          
                        