#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-26下午6:03:31
usege:

"""

import pexpect 
import paramiko
import traceback
 


def trace_back():
    try:
        return traceback.format_exc()
    except:
        return ''
    
__all__ = ['Custom_scp']

#设置日志记录
paramiko.util.log_to_file('./Custom_scp')

class Custom_scp(object):
    '''
     pexpect 不可并发执行，只能单进程执行
     且拦截password时，不同系统有大小写问题
    '''
    
    def __init__(self):
        pass
     
    @staticmethod
    def get(user,host,route_from,route_to,passwd):  
        
        cmd = "scp -r %s@%s:%s %s"%(user,host,route_from,route_to)  
        print cmd  
        ssh = pexpect.spawn(cmd,timeout=1200)  
        try:  
            i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)  
            if i == 0 :  
                ssh.sendline(passwd)  
            elif i == 1:  
                ssh.sendline('yes\n')  
                ssh.expect('password: ')  
                ssh.sendline(passwd)  
            ssh.sendline(cmd)  
            r = ssh.read()  
            print r  
            ret = 0 
        except pexpect.EOF:  
            print "EOF" 
            ssh.close()  
            ret = -1 
        except pexpect.TIMEOUT:
        
            print "TIMEOUT" 
            ssh.close()  
            ret = -2   
        return ret 
    
    
    @staticmethod      
    def put(route_from,user,host,route_to,password):  
        cmd = "scp -r %s %s@%s:%s"%(route_from,user,host,route_to)  
        print cmd  
        ssh = pexpect.spawn(cmd)  
        try:  
            i = ssh.expect(['Password:', 'continue connecting (yes/no)?'], timeout=5)  
            if i == 0 :  
                ssh.sendline(passwd)  
            elif i == 1:  
                ssh.sendline('yes\n')  
                ssh.expect('Password: ')  
                ssh.sendline(passwd)  
            ssh.sendline(cmd)  
            r = ssh.read()  
            return {'flag':'1','ip':self.host['ip'],'data':r} 
        except pexpect.EOF:  
            print "EOF" 
            ssh.close()  
            return {'flag':'0','ip':self.host['ip'],'data':trace_back()}  
        except pexpect.TIMEOUT:  
            print "TIMEOUT" 
            ssh.close()  
            return {'flag':'0','ip':self.host['ip'],'data':trace_back()}  
        
    def __del__(self):
        pass



  
