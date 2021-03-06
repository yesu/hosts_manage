#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-26下午6:03:31
usege:

"""
import os
import paramiko
import commands
import traceback
from multiprocessing  import Process
from threading import  Thread

from custom.db.mysql import Custom_MySQL 

def trace_back():
    try:
        return traceback.format_exc()
    except:
        return ''
    
__all__ = ['Custom_ssh']

#设置日志记录
paramiko.util.log_to_file('/tmp/test')

class Custom_ssh(Thread):
    
    
    def __init__(self,grandchild,**host):
        Thread.__init__(self)
        self.host = host
        self.result = {}
        self.grandchild = grandchild
        
    def run(self):
        db = Custom_MySQL(using='log')
        status = {'flag':1}
        db.update('batch_detail',
                  'batch_id="%s" and ip ="%s"'  % (self.host['batch_id'],self.host['ip']),
                  **status)
        db.commit()
        db.close()
        try:
             
            #建立连接
            self.ssh=paramiko.SSHClient()
            
            #如果没有密码就走public key
            if self.host.get('pwd',True) == True:
                privatekeyfile = os.path.expanduser('/root/.ssh/id_rsa')
                paramiko.RSAKey.from_private_key_file(privatekeyfile)
    
            #缺失host_knows时的处理方法
            known_host = "/root/.ssh/known_hosts"
            self.ssh.load_system_host_keys(known_host)
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
            #os.system('/opt/local/junos/junos')
            #连接远程客户机器
            self.ssh.connect(
                        hostname =self.host['ip'],
                        port     =int(self.host['port']),
                        username =self.host['user'],
                        password =self.host['pwd'],
                        compress =True,
                        timeout  =20
                        )
         
            #获取远程命令执行结果
            stdin, stdout, stderr = self.ssh.exec_command(self.host['cmd'],bufsize=65535, timeout=10)
            temp = stdout.readlines()
            
            db = Custom_MySQL(using='log')
            status = {'flag':2,'result':''.join(temp)}
            db.update('batch_detail',
                      'batch_id="%s" and ip ="%s"' % (self.host['batch_id'],self.host['ip']),**status)
            db.commit()
            db.close()
           
            
            if temp ==[]:
    
                self.grandchild.put({'flag':'1','ip':self.host['ip'],'data':temp})
            else:
                self.grandchild.put({'flag':'0','ip':self.host['ip'],'data':temp})
            #输出执行结果
            self.ssh.close()
            
        except  :
            #print trace_back()
            #以防paramiko本身出问题，这里再用shell运行一次，如果还出问题再确认为问题
            cmd ="ssh -p %s -o StrictHostKeyChecking=no %s@%s  %s"%(self.host['port'],self.host['user'],self.host['ip'],self.host['cmd'])
            (status,output) = commands.getstatusoutput(cmd)
            if status == 0:
                db = Custom_MySQL(using='log')
                status = {'flag':2,'result':output}
                db.update('batch_detail',
                          'batch_id="%s" and ip ="%s"' % (self.host['batch_id'],self.host['ip']),
                          **status)
                db.commit()
                db.close()
            
                self.grandchild.put({'flag':'1','ip':self.host['ip'],'data':output})
            else:
                
                db = Custom_MySQL(using='log')
                status = {'flag':-1,'result':'faild'}
                db.update('batch_detail',
                          'batch_id="%s" and ip ="%s"' % (self.host['batch_id'],self.host['ip']),
                          **status)
                db.commit()
                db.close()
            
                self.grandchild.put({'flag':'0','ip':self.host['ip'],'data':trace_back()})
            
    def ret_result(self):
         
         return self.result       

        
    def __del__(self):
        pass
