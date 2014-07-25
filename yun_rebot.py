#/usr/bin/python evn
#coding=utf-8


import os
from  assets import assets
from  yun.api import api
from  yun_manage import yun_manage 

def run(yun_name):
    
    strat1 = api(yun_name,'get_idcs')
               
    data = strat1.get_result()
    #print data
    yun1 = yun_manage()
    yun1.data =data
    yun1.save_idcs()
       
    for idc in assets.get_idcs(yun_name):
        print idc
        t = api(yun_name,'get_hosts',idc)
        data =  t.get_result()
        print data
        yun1 = yun_manage()
        yun1.data =data
        yun1.save_hosts()
    
   
    for idc in assets.get_idcs(yun_name):
        print idc
        t = api(yun_name,'get_balancers',idc)
        data =  t.get_result()
        print data
        yun1 = yun_manage()
        yun1.data =data
        yun1.save_balancers()  
            
if __name__ == '__main__':
    

    yun_list = ['amazon','aliyun','ucloud']
     
    for yun in yun_list:
         
        run(yun)


   
   