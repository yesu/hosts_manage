#!/usr/bin/python
#coding=utf-8


import string

from multiprocessing  import Process
import time
import datetime
import os
import signal
from pprint import pprint
from multiprocessing  import JoinableQueue,active_children
from threading import  Thread

__all__ = ['Master']


class Master(Process):

    grandchild = JoinableQueue()
    
    def __init__(self,bus,child_conn,child_timeout=60):

        super(Master,self).__init__()
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.child_timeout = child_timeout
        self.bus = bus
        self.child_conn = child_conn
        self.child_process = []
        self.flag =0
        self.child_num = 10
        
        

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
        print 'ssh num:%s'% num
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
            if i.is_alive():
                return False
        return True
    
    def run(self):
        
        from custom.command.remote.ssh import Custom_ssh
        
        #        
        for bus in self.bus:
        #while len(self.bus):
            #bus = self.bus.pop()
            if self.__check_active_children():
                time.sleep(0.5)
                print bus['ip'],bus['port'],bus['user']
                temp = Custom_ssh(Master.grandchild,**bus)
                #temp.setDaemon(True)
                temp.start() 
                self.child_process.append(temp)
                
            
       
    
        while 1:
            
            time.sleep(10)
            if self.__check_child_is_alive():
                
                temp = []
                for i in self.child_process:
                    print 'master child over'
                    temp.append(Master.grandchild.get())
                    Master.grandchild.task_done()
                self.child_conn.put(temp)
                
                break
            
            if self.check_timeout():
                print 'kill master child'
                temp = []
                for i in self.child_process:
                    if i.is_alive():
                       
                        try:
                            temp.append(Master.grandchild.get(timeout=30))
                            Master.grandchild.task_done()
                        except:
                            temp.append([])
                        
                        #os.kill(i.pid,signal.SIGKILL)
                    else:
                        temp.append(Master.grandchild.get())
                        
                        Master.grandchild.task_done()
                       
                self.child_conn.put(temp)
 
                break
        
        exit(0)         




    def kill_child(self):


        for i in self.child_process:
            if i.is_alive():
                os.kill(i.pid,signal.SIGKILL)
                        
        try:
            self.terminate()
        except:
            pass

        try:

            os.kill(self.pid,signal.SIGKILL)
        except:
            pass
        
            #print 'grandson is over ,kill it again'
