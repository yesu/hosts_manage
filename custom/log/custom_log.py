#!/usr/bin/python
#coding:utf-8
"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-1下午12:24:29
usege:

"""

import sys, os, re
import logging
import logging.handlers


class LogFactory:
    
    '''日志工厂'''
    
    ilog = None #信息日志
    elog = None #错误日志
    root = os.path.abspath('.')
    ilogfile = root+'/logs/mtask_info_%s.log' #信息日志文件
    elogfile = root+'/logs/mtask_err_%s.log' #错误日志文件
    ERROR = 'err'
    INFO = 'info'

    @staticmethod
    def init_log(logtype, p = ""):
        '''
        初始化日志对像
        @param logtype:info 和 err分别是信息日志和错误日志
        @param p :日志文件名后缀
        '''

        logfile = LogFactory.ilogfile % p
        if logtype == LogFactory.ERROR: logfile = LogFactory.elogfile % p
        logger = logging.getLogger(logtype)
        logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024*1024, backupCount=5)

        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s %(lineno)d %(message)s')

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger


    @staticmethod
    def get_err_logger(p=""):
        '''初使化错误日志'''
        if not LogFactory.elog :
            LogFactory.elog = LogFactory.init_log(LogFactory.ERROR, p)
        return LogFactory.elog

    @staticmethod
    def get_info_logger(p=""):
        '''初使化错误日志'''
        if not LogFactory.ilog :
            LogFactory.ilog = LogFactory.init_log(LogFactory.INFO, p)
        return LogFactory.ilog




def w_info(msg,p=''):
    '''
    写信息日志
    @param msg:信息
    '''
    ilogger = LogFactory.get_info_logger(p=p)
    ilogger.info(msg)
def w_err(msg,p=''):
    '''
    写错误日志
    @param msg : 错误信息
    '''
    elogger = LogFactory.get_err_logger(p=p)
    elogger.error(msg)