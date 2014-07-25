#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-26下午6:03:31
usege:

"""

import paramiko
import traceback
import socket
import time

def trace_back():
    try:
        return traceback.format_exc()
    except:
        return ''
    
__all__ = ['Custom_ssh']

#设置日志记录
paramiko.util.log_to_file('/tmp/test')

class Custom_cmd(object):
    
    def __init__(self,**host):
        self.host = host
        self.error = ''
        
    def run(self,cmd):
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host['ip'],self.host['port']))
            #设置ssh连接的远程主机地址和端口
            self.t=paramiko.Transport(self.sock)
            #设置登录名和密码
            self.t.connect(username=self.host['user'],password=self.host['pwd'])
            #连接成功后打开一个channel
            self.chan=self.t.open_session()
            #设置会话超时时间
            self.chan.settimeout(120.0)
            #打开远程的terminal
            self.chan.get_pty()
            #激活terminal
            self.chan.invoke_shell()

            self.chan.send(cmd+'\n')
            
            #out =''
            tCheck = 0
            while not self.chan.recv_ready():
                time.sleep(5)
                tCheck+=1
                if tCheck >= 6:
                    print 'time out'#TODO: add exeption here
                    return False
       
             
          
            return {'flag':'1','ip':self.host['ip'],'data':self.chan.recv(65535)}
            #输出执行结果
            self.chan.close()
  
            self.t.close()
        except:
            return {'flag':'0','ip':self.host['ip'],'data':trace_back()}
            exit()
            

        
    def __del__(self):
        pass
