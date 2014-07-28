#!/usr/bin/env python
#coding=utf-8
import socket  
import time
import sys
import multiprocessing

pool = multiprocessing.Pool(processes=4)
result = []

for url in urls:
   
    result.append(pool.apply_async(readhtml, (url, )))
pool.close()
pool.join()
for res in result:
    print res.get()

    
def clint():
     host = '203.90.236.112'
     port = 32777
     bufsize = 1024
     addr = (host,port)
     client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     client.connect(addr)

          
     data ='中国人 7888888'                  
     client.send(data)

     client.close() 

if __name__ == '__main__':   
    clint()                 