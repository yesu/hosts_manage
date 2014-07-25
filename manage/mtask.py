#!/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-2下午4:45:23
usege:

"""
import math
from multiprocessing  import Process,Pool,Pipe,cpu_count,active_children,JoinableQueue
import time
from itertools import izip
import random
import datetime
import os,sys
import signal
from threading import Thread
import threading
from manage.master import Master
from custom.log.custom_log import w_info,w_err
import multiprocessing
import logging
from custom.db.mysql import Custom_MySQL 
from pprint import pprint 
#设置一下递归大小
sys.setrecursionlimit(1000000)

__all__ = ['Mtask']

class Mtask(Process):
    '''
    主进程类 为了兼容windows而这样创建类
    '''

    

    def __init__(self,cmd_param):
        '''
        主进程类 为了兼容windows而这样创建类
        '''
        super(Mtask,self).__init__()
        self.start_time = datetime.datetime.now()
        self.parent_timeout = 240
        self.parent_timeout_flag = 0
        self.child_timeout =180
        self.child_num = 100
        self.slice_num = 20
        self.process_list = []
        self.result =[]
        self.batch_id = 0
        self.print_flag = 1
        self.mult_debug_flag = 0
        self.cmd_param = cmd_param
       


        if self.mult_debug_flag:
            #设置进程log日志
            multiprocessing.log_to_stderr()
            logger=multiprocessing.get_logger()
            logger.setLevel(logging.INFO)

    def __kill_child(self):
        '''
        杀子进程
        '''

        for process in  self.process_list:
            
            #主进程超时，子进程未完成
            if process.is_alive():
                
                if self.print_flag:
                    print 'kill son'

                process.kill_child()
                #process.terminate()
                os.kill(process.pid,signal.SIGKILL)

            #主进程超时时，子进程已完成的状况
            else:
                if self.print_flag:
                    print 'son process is die'#'子进程已死'




    def __kill_current_process(self):
        '''当前进程自杀'''

        if self.is_alive():
            #self.terminate()
            os.kill(os.getpid(), signal.SIGKILL)
            os._exit(1)


    def __check_active_children(self):
        '''
        检查进程数，不超标
        '''

#         num = 0
#         #根据实际的继承类，用不同的方法统计存活子类数
#         for i in self.process_list:
#             if isinstance(i, Thread):
#                 if i.isAlive():
#                     num = num +1
#                     
#             if isinstance(i, Process): 
#                 if i.is_alive():
#                     num = num +1
#         #print 'master num:%s'% num
        if len(active_children()) >= self.child_num:
            
            time.sleep(1)
            
            self.__check_active_children()
        else:
            return True

    def before(self):
        if self.mult_debug_flag:
            print 'before call start, please rewrite this method'#'前置调用开始,业务类请重写此方法'
        pass

    def after(self):
        if self.mult_debug_flag:
            print 'before call start, please rewrite this method'#'后置调用开始，业务类请重写此方法'
        pass

    def get_result(self):
        '''
        获取子进程执行结果
        '''
        db = Custom_MySQL(using='log')
        result = db.query('select ip,result as data,IF(flag=2,1,0) as flag \
                           from batch_detail \
                           where batch_id ="%s"'% self.batch_id )
        db.close()
        print '===========', len(result),'================'
        self.result = result
        



    def check_timeout(self):
       
        end_time = datetime.datetime.now()
        interval=(end_time - self.start_time).seconds

 
        if interval >=self.parent_timeout:
            return True
        else:
            False
    #将list对象N等分
    def div_list(self,ls,n):
        if not isinstance(ls,list) or not isinstance(n,int):
            return []
        ls_len = len(ls)
        if n<=0 or 0==ls_len:
            return []
        if n > ls_len:
            return []
        elif n == ls_len:
            return [[i] for i in ls]
        else:
            #int(math.ceil(lent/self.slice_num))+1
            j = int(math.ceil(ls_len/n))+1
            k = int(math.ceil(ls_len%n))+1
            ### j,j,j,...(前面有n-1个j),j+k
            #步长j,次数n-1
            ls_return = []
            for i in xrange(0,(n-1)*j,j):
                ls_return.append(ls[i:i+j])
            #算上末尾的j+k
            ls_return.append(ls[(n-1)*j:])
            return ls_return
               
    def run(self):
        '''
        运行函数
        @param bus_list:业务列表
        '''


        if self.parent_timeout < self.child_timeout:
            if self.print_flag:
                print 'parents times loss son times, please try it(%s:%s）' % (self.parent_timeout,self.child_timeout)#'父进程超时间比子进程超时间小，请重新设置（%s:%s）' % (self.parent_timeout,self.child_timeout)
            w_info('父进程超时间比子进程超时间小，请重新设置（%s:%s）' % (self.parent_timeout,self.child_timeout))
            #退出
            os.kill(os.getpid(), signal.SIGKILL)
            os._exit()
        try:
            self.before()
        except Exception, e:
            if self.print_flag:
                print 'before call method error'#'前置调用函数有错误'
            w_info('前置调用函数有错误：%s' % e)
            #退出
            os.kill(os.getpid(), signal.SIGKILL)
            os._exit()
            
           
        #数据库不支持事务处理
        db = Custom_MySQL(using='log')
       
        #将前端传送过的作业，加上ip 标上批次记入数据库
        last_insert_id =  db.insert('batch',**{})
        self.batch_id = last_insert_id
        db.commit()

        for  task in self.cmd_param:
            task['batch_id'] = last_insert_id
            detail ={}
            
            detail['batch_id'] = last_insert_id
            detail['ip'] = task['ip']
            detail['cmd'] = task['cmd']
            detail['flag'] = 0
            
            db.insert('batch_detail',**detail)
        db.commit()
        
          
        lent = len(self.cmd_param)

        temp_list = self.div_list(self.cmd_param, self.child_num)
        print '共有任务: %s 条,共产生: %s 批次任务'% (lent,len(temp_list))    
        
        #os.popen('/opt/local/junos/junos')  
        #为每个区组启子进程
        for bus in temp_list:
        #while len(temp_list):
            #bus = temp_list.pop()
            #进程数检查
            if self.__check_active_children():
                
                #开启子进程
                process = Master(bus,self.child_timeout)
              
                #主进程超时检查
                #主进程超时时，子进程并未启动的情况
                if self.check_timeout():
                    self.parent_timeout_flag =1
                    continue
    

                process.start()

                self.process_list.append(process)


        print u'进程加载完毕等待进程结束'
        while 1:

            time.sleep(1)
            #设置超时
            end_time = datetime.datetime.now()
            interval=(end_time - self.start_time).seconds

            #超时情况
            if interval >=self.parent_timeout:
                if self.print_flag:
                    #'有子进程未完成，需要手工杀掉'
                    print u'父类超时,可能存在子进程未完成，需要手工杀掉'
                self.__kill_child()
                break
     
                
            #非超时
            else:
                #子进程已执行完毕
                if len(active_children()) == 0:
                    if self.print_flag:
                        print 'all process is over'#'所有子进程已完成'
                    self.__kill_child()


                    try:
                        self.after()
                    except Exception, e:
                        if self.print_flag:
                            print 'after call method error'#'后置调用函数有错误'
                        w_info('后置调用函数有错误%s' % e)

                    break
                #子进程未执行完毕
                else:

                    continue

