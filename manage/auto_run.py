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



from abc import ABCMeta  
from abc import abstractproperty
from abc import abstractmethod 


class Custom_Interface(object):
    
    __metaclass__ = ABCMeta



    @abstractmethod
    def run(self):

        return
    
    @abstractmethod
    def get_result(self):
        return
    
    @abstractmethod
    def call_back(self):
        return
        
class auto_run(Mtask,Custom_Interface):
    
    
    def run(self):
        super(auto_run, self).run()
        
        self.call_back(self.get_result())
    
    def get_result(self):
        super(auto_run, self).get_result()
        
        return self.result