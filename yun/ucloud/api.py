#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-13 11:55:57
usege:

"""
import time
from pprint import pprint
from threading import  Thread
from multiprocessing import Process
from api_base import UcloudApiClient

__ALL__ =['API']

class API(Process):
    
    def __init__(self,func,**param):
        super(API,self).__init__()
        self.func = func
        self.param = param
        self.result = []
        
    def  run(self):
        '''
        任务调度，根据不函数名不同进行任务作业
        '''
        if callable(getattr(self ,self.func)):
            if isinstance(self.param,dict) and self.param !={}:
                self.result = getattr(self, self.func)(**self.param)
            else:
                self.result = getattr(self, self.func)()
    
    def get_idcs(self): 
        '''
        ucloud没有提供此接口
        '''
        
        param ={}
        param['area']=u'双线'
        param['name'] = u'ucloud-yun[北京BGP A]'
        param['prefix']= '1001'
        self.result.append(param)
        
        param ={}
        param['area']=u'双线'
        param['name'] = u'ucloud[亚太]'
        param['prefix']= '3001'
        self.result.append(param)
           
        return self.result
    
      
    def get_hosts(self,**idc_dict):
        '''
        获取主机内容 
        '''
        idc =  idc_dict['prefix']
        del idc_dict['prefix']
        
        ApiClient = UcloudApiClient(region_id =idc)
        result = ApiClient.get("/instances", offset=0, max_count=50)
        pprint((result['data']))
        for host in result['data']:
            
            public_ip = ''
            inner_ip = ''
            
            if host.get('public_ip'):
                public_ip = host['public_ip'][0]
            if host.get('private_ip'):
                
                inner_ip = host['private_ip'][0]

            param={}
            param['public_ip']  = public_ip
            param['hostname']   = host['hostname']
            param['wxsn']       = host['vmid']
            param['inner_ip']   = inner_ip
            param['purchase_date'] = time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(host['create_time']))
            param.update(idc_dict)
            
            self.result.append(param)
            
        return self.result



    def get_balancers(self,**idc_dict):
        
        idc =  idc_dict['prefix']
        del idc_dict['prefix']
        
        ApiClient = UcloudApiClient(region_id =idc)
        result = ApiClient.get('/ulb/vserver', offset=0, max_count=10);
      
        
        if result['ret_code']==0 and result.get('data',None)!=None:
            
            for balancer in result['data']:
                
                
                public_ip = ''
                inner_ip = ''
                
                if balancer.get('public_ips'):
                    public_ip = balancer['public_ips'][0]['ip']
                #保存代理服务器与后端服务器关系    
                children = []
                for child in  balancer['vserver_infos']['server_infos']:
                    children.append(child['server_id'])
                    
                #print count
                param={}
                param['public_ip'] = public_ip
                param['hostname']  = balancer['vip_name']
                param['wxsn']      = balancer['vip_id']
                param['idc_id']    = idc_dict['idc_id']
                param['children']  = ','.join(children)
                
                self.result.append(param)
            
        return self.result        


    def get_result(self):
        
        return self.result
 
