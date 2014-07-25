#!/usr/bin/python
#coding=utf-8


import json
import urllib2
import urllib
from urllib2 import  URLError


def get(url,charset ='utf-8',debug=0):
    
    httpHandler = urllib2.HTTPHandler(debuglevel=debug)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=debug)
    opener = urllib2.build_opener(httpHandler, httpsHandler)

    urllib2.install_opener(opener)
    req = urllib2.Request(url)

    req.add_header('User-Agent',"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0")
    req.add_header('charset', charset)

    try:
        response = urllib2.urlopen(req)
        data = response.read()
        return "".join(data)
        
    except URLError, e:
        print e.code
        print e.read()
        
def ajax(url,data,referer=None,**headers):
        '''
        模拟浏览器ajax请求
        ''' 
     
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        req.add_header('X-Requested-With','XMLHttpRequest')
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116')
        if referer:
            req.add_header('Referer',referer)
        if headers:
            for k in headers.keys():
                req.add_header(k,headers[k])
    
        params = urllib.urlencode(data)
        response = urllib2.urlopen(req, params)
        jsonText = response.read()
        return json.loads(jsonText)