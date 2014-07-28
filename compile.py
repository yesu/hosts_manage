#-*- coding=utf-8
'''
#编译目录下所有py文件为 pyc文件
import compileall
compileall.compile_dir(r"d:\python")  #r"d:\python" 路径
'''
#编译 单个py文件为 pyc文件

import py_compile
py_compile.compile(r"/root/hosts_manage/monitor/client.py") # r"d:\python\test.py":路径