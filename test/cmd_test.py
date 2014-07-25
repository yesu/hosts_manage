import pexpect  
import traceback  
 
def ssh_cmd(ip, passwd, cmd):  
    ret = -1 
    ssh = pexpect.spawn('ssh playcrab@%s "%s"' % (ip, cmd))  
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

def scp_from(user,host,route_from,route_to,passwd):  
    
    cmd = "scp -r %s@%s:%s %s"%(user,host,route_from,route_to)  
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
  
def scp_to(route_from,user,host,route_to,password):  
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
    
ssh_cmd('172.16.30.50','123456','df -h')
scp_from('playcrab','172.16.30.50','/var/log/system.log','/tmp/','123456')
