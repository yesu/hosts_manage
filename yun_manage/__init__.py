# /usr/bin/python evn
# coding=utf-8
import sys
sys.path.append("../")

import json
from custom.db.mysql import Custom_MySQL



class Desc(object):
    "A descriptor example that just demonstrates the protocol"

    def __get__(self, obj, cls=None): 
            pass

    def __set__(self, obj, val):
            pass

    def __delete__(self, obj): 
            pass
                
class yun_manage():
    
    
    data = Desc()
        
         
            
    def save_idcs(self):
        
        if self.data == None:
            return False
        
        db = Custom_MySQL(using='center_app')
        
        
        for  param in  self.data:
            
            sql = 'select count(*) as count from idc where prefix = %s'
            p = (param['prefix'],)
            count = db.count(sql, *p)
            # 检查是否存在
            if count['count'] == 0:      
                db.insert('idc', **param)
            else:
                db.update('idc', 'prefix="%s"' % param['prefix'], **param) 
            

    def save_hosts(self):
        
        if self.data == None:
            return False
                
        db = Custom_MySQL(using='center_app')

        for param in self.data:

            sql ='select count(*) as count from assets where wxsn= %s'
            p =(param['wxsn'],)
            count = db.count(sql,*p)

 
            if count['count'] == 0:
                db.insert('assets',**param)
            else:
                db.update('assets','wxsn="%s"'%param['wxsn'],**param)  
                 
    def save_balancers(self):
        
        if self.data == None:
            return False
                
        db = Custom_MySQL(using='center_app')
        
        for param in self.data:
            
            sql ='select count(*) as count from assets where wxsn= %s'
            p =(param['wxsn'],)
            count = db.count(sql,*p)


        
            if count['count'] ==0:
                db.insert('assets',**param)
            else:
                db.update('assets','wxsn="%s"'%param['wxsn'],**param)   
                    
                        