#!/usr/bin/python
#coding=utf-8


import string

from multiprocessing  import Process
import time
import datetime
import os,sys
import signal
from pprint import pprint
from multiprocessing  import JoinableQueue,active_children
from threading import  Thread
#设置一下递归大小
sys.setrecursionlimit(1000000)

__all__ = ['Master']


class Master(Process):

    
    def __init__(self,bus,child_timeout=60):

        super(Master,self).__init__()
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.child_timeout = child_timeout
        self.bus = bus
        self.child_process = []
        self.flag =0
        self.child_num = 3
        
        

    def __check_active_children(self):
        '''
        检查进程数，不超标
        '''
    
        num = 0
        #根据实际的继承类，用不同的方法统计存活子类数
        for i in self.child_process:
            if isinstance(i, Thread):
                if i.isAlive():
                    num = num +1
                     
            if isinstance(i, Process): 
                if i.is_alive():
                    num = num +1
        
        if num >= self.child_num:
            
            time.sleep(1)
            
            self.__check_active_children()
        else:
            return True
        
    def check_timeout(self):
        
        end_time = datetime.datetime.now()
        interval=(end_time - self.start_time).seconds

        
        if interval >=self.child_timeout:
            return True
        else:
            False
            
    def __check_child_is_alive(self):
        '''
        检查子是否还有存活的
        '''
        for i in self.child_process:
            if isinstance(i, Thread):
                if i.isAlive():
                    return False
                     
            if isinstance(i, Process): 
                if i.is_alive():
                    return False
                
        return True
    
    def run(self):
        
        from custom.command.remote.ssh import Custom_ssh
        
        index = 1       
        for bus in self.bus:

            if  index >= self.child_num:
                time.sleep(10)
                index = index -2
                
            print bus['ip'],bus['port'],bus['user']
            temp = Custom_ssh(**bus)
            #temp.setDaemon(True)
            temp.start() 
            self.child_process.append(temp)
            index = index +1
                
            
       
        print '%s load work finish '% self.name
        while 1:
            time.sleep(1)
            if self.__check_child_is_alive() == True:

                break
            
            elif self.check_timeout() == True:

                break
       


    def kill_child(self):
     
        try:
            self.terminate()
        except:
            pass

        try:

            os.kill(self.pid,signal.SIGKILL)
        except:
            pass

