#/usr/bin/python
#coding=utf-8

import types
import json

from custom.auto_load import auto_load


class api():
    '''
    本模块自动加载yun中的不同的模块类型，并运行，与实际业务无关，放置在yun包中
    '''
    def __init__(self,package_name,func_name,param ={}):
        
        self.package_name = package_name
        self.func_name    = func_name
        self.param        = param
        self.mod          = None
            
    def get_mod(self):
        
        #自动加载模块
        auto = auto_load('yun.%s.api'%self.package_name)   
        self.mod = auto.get_mod() 
        
    def get_result(self): 
        
        self.get_mod()

        #实例化 运行
        object = None
        
        if self.param == {}:
            
            object = getattr(self.mod, 'API')(self.func_name)
        else:
            
            object = getattr(self.mod, 'API')(self.func_name,**self.param)
            
        object.start()
        object.join()
        
        return object.get_result()
