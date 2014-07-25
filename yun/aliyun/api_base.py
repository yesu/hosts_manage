#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys,os
import urllib, urllib2
import urllib3
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
from custom.config.ini import DictConfigParser


ini_path = os.path.join(os.path.abspath('./config/'),'yun_config')

ini_section_key  ='aliyun'



def percent_encode(str):
    res = None
    try:
        res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    except:
        
	res = str

    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    
    n = DictConfigParser(ini_path)
    access_key_id = n[ini_section_key]['id'].encode('utf-8')
    access_key_secret = n[ini_section_key]['key'].encode('utf-8')
    ecs_server_address = n[ini_section_key]['url'].encode('utf-8')
    
    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2013-01-10', \
            'AccessKeyId'   : access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
    }

    for key in user_params.keys():
        parameters[key] = user_params[key]

    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = ecs_server_address + "/?" + urllib.urlencode(parameters)
    return url

def make_request(user_params, quiet=False):
    url = compose_url(user_params)
    
    
    #替一个线程安全函数
    http = urllib3.PoolManager()
     
    r = http.request('get',url)
    
    if r.status != 200:
        
        raise SystemExit(r.data)
    
    response = r.data
    
#     request = urllib2.Request(url)
 
#     try:
#         conn = urllib2.urlopen(request)
#         response = conn.read()
#     except urllib2.HTTPError, e:
#         print(e.read().strip())
#         raise SystemExit(e)

    #make json output pretty, this code is copied from json.tool
    try:
        obj = json.loads(response)
        if quiet:
            return obj
    except ValueError, e:
        raise SystemExit(e)
    json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write('\n')


def describe_instances(regionid):

    if isinstance(regionid,dict):
        return make_request(regionid,quiet=True)
        
    
    user_params = {}
    user_params['Action'] = 'DescribeZones'
    user_params['RegionId'] = regionid
    obj = make_request(user_params, quiet=True)
    
    zones = []
    #print('%21s %21s %10s %15s' % ('InstanceId', 'InstanceName', 'Status', 'InstanceType'))
    for zone in obj['Zones']['Zone']:
        user_params = {}
        user_params['Action'] = 'DescribeInstanceStatus'
        user_params['RegionId'] = regionid
        user_params['ZoneId'] = zone['ZoneId']
        user_params['PageSize'] = '50'
        user_params['PageNumber']= '1'

        instances = make_request(user_params, quiet=True)
        if len(instances) > 0:
            for i in instances['InstanceStatuses']['InstanceStatus']:
                instanceid = i['InstanceId']
                params = {}
                params['Action'] = 'DescribeInstanceAttribute' 
                params['InstanceId'] = instanceid
                res = make_request(params, quiet=True)
                res['ZoneId'] = zone['ZoneId']
                zones.append(res)
                #print('%21s %21s %10s %15s' % (res['InstanceId'], res['InstanceName'], res['Status'], res['InstanceType']))
                
    return zones

def DescribeLoadBalancers(regionid):
    user_params = {}
    user_params['Action'] = 'DescribeLoadBalancers'
    user_params['RegionId'] = regionid
    obj = make_request(user_params, quiet=True)
    

    zones = []

    for balancer in obj['LoadBalancers']['LoadBalancer']:
        user_params = {}
        user_params['Action'] = 'DescribeLoadBalancerAttribute'
        user_params['LoadBalancerId'] = balancer['LoadBalancerId']

        instances = make_request(user_params, quiet=True)
        if len(instances) > 0:
            zones.append(instances)
                
    return zones