#/usr/bin/python
#coding=utf-8

'''
auth:wuqichao@playcrab.com
date:2014-06-17 12:00

'''
import time
from pprint import pprint
from assets import assets
from manage.cmd import manage_cmd


            


if __name__ == '__main__':
    
    n = manage_cmd()
    manage_cmd.result = assets.get_assets()
    manage_cmd.cmd = """grep -c 'model name' /proc/cpuinfo"""
    n.run()
    
