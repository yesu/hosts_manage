#!/usr/bin/python
#coding=utf-8
"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-25下午5:20:27
usege:

"""


import json,time
import sys,os,string
import socket, select
import threading,Queue
import syslog


port = 8010
buf_size = 1024

APPDIC = {}
CURR_TIME_STAMP = 0

queue = Queue.Queue()
lock = threading.RLock()

class Thwork(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        global APPDIC
        global CURR_TIME_STAMP
        global queue
        while True:
            lock.acquire()
            (fileno,result) = queue.get(block = True)
            lock.release()
            try:
                print 'sssssssssss'
                print fileno,result
            except Exception, e:
                w_log(json.dumps(e.args))


#初始化池
def addjob(fno, data):
    global queue,gcnum
    queue.put((fno, data))

#经两次fork实现脱终端，成为守护进程
def daemon():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        os.setsid()
        os.umask(0)
        pid = os.fork()
        if pid > 0: # exit from second parent
            sys.exit(0)


        for i in range(65):
            try:
                os.close(i)
            except:
                continue

        sys.stdin = open("/dev/null", "r+")
        sys.stdout = sys.stdin
        sys.stderr = sys.stdin

    except OSError, e:
        w_log("fork failed: (%s)" % e)
        sys.exit(1)

    main()


def main():
    #开启向外部应用发送信息的新线程
    
    t_work = {}
    for i in range(4):
        t_work[i] = Thwork()
        t_work[i].start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))
    sock.listen(10240)
    sock.setblocking(0)

    epoll = select.epoll(10240)
    epoll.register(sock.fileno(), select.EPOLLIN | select.EPOLLET)


    try:
        clients = {} ;results = {}
        while True:
            try:
                events = epoll.poll(0.1)
                for fileno, event in events:
                    if fileno == sock.fileno():
                        while True:
                            try:
                                client, addr = sock.accept()
                            except:
                                break
                            client.setblocking(0)
                            epoll.register(client.fileno(), select.EPOLLIN | select.EPOLLET)
                            clients[client.fileno()] = client
                            results[client.fileno()] = ''

                    elif event & select.EPOLLIN:
                        while True:
                            try:
                                tmp = clients[fileno].recv(buf_size)
                            except:
                                break

                            if tmp == '':
                                epoll.unregister(fileno)
                                address = clients[fileno].getpeername()[0]
                                clients[fileno].close()
                                del clients[fileno]
                                if results.has_key(fileno):
                                    addjob(address, results[fileno])
                                del results[fileno]
                                break

                            results[fileno] += tmp

                    elif event & select.EPOLLHUP or event & select.EPOLLERR:
                        epoll.unregister(fileno)
                        clients[fileno].close()
                        del clients[fileno]
                        del results[fileno]

            except Exception, msg:
                w_log("%s" %msg)

    finally:
        epoll.unregister(sock.fileno())
        epoll.close()
        sock.close()

def w_log(msg):
    syslog.syslog(syslog.LOG_ERR, msg)

if __name__ == '__main__':
    main()
#     syslog.openlog("monitor_svr", 0, syslog.LOG_LOCAL6)
#     daemon()
#     syslog.closelog()
