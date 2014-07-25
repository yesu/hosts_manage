#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-13 11:55:57
usege:

"""

import json
import urllib
import urllib2
from pprint import pprint
from  multiprocessing import Process


from custom.db.mysql import Custom_MySQL
from config.api_config import game
 
__ALL_ = ['Rebot_Game_Info']


def cmd5(data):
     '''
     md5
     '''
     import md5
     m= md5.new()
     m.update(data)
     return m.hexdigest()
 
  
            

class Rebot_Game_Info(Process):

   
    def __init__(self,game_code,platform):
        
        Process.__init__(self)
        self.game_code = game_code
        self.platform = platform
        self.api_url = game[self.game_code][self.platform]
        
        
    def request_ajax_data(self,url,data,referer=None,**headers):
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
    
    
    def create_token(self):
        '''
        生成请求用的key
        '''
           
       

        try:
            #key =md5(域名＋游戏代号)
            domain =game[self.game_code][self.platform].split('//')[1].split('/')[0]
            
            return cmd5(domain+self.game_code)
        
        except Exception as e:
            print e
            return None

            
    def assets2appinfo(self):
        
        db = Custom_MySQL(using='center_app')
        #将assets中有的，但是在app_info没有的，插入到app_info中
        sql ='''
            INSERT into app_info (assets_id,name,public_ip,inner_ip,main_category_id)
            SELECT id,hostname as name,public_ip,inner_ip,main_category_id
            from 
            assets
            where public_ip 
            not in (select public_ip from app_info )
            '''
        db.execute(sql) 
        db.commit()
        
    def get_api_data(self):
           
        token = self.create_token()
        
        #如果key没有生成退出
        if token == None:
            exit()
        print self.api_url
        
        #获取json数据
        result = self.request_ajax_data(self.api_url,{'key':token})
        
        

        if int(result['flag']) == 0:
            return None
        else:
            return result['data']
   
    def insert_db(self,main_category_id,sub_category_id,platform,app):
        
                          
        temp_app ={}
        temp_app['name']=app['type']+'['+app['memo']+']'
        temp_app['platform'] = platform
        temp_app['type']=app['type']
        temp_app['port']=app['port']
        temp_app['main_category_id'] = main_category_id
        temp_app['sub_category_id'] = sub_category_id
        if app.get('db_type',False):
            temp_app['db_type'] = app['db_type']
        
        sql ='select count(*) as count from app_info where '
        #同一游戏同一区组 
        where ='type="%s" and port="%s"  and main_category_id="%s" \
        and sub_category_id="%s"'% (app['type'],app['port'],main_category_id,sub_category_id) 
         
        db = Custom_MySQL(using='center_app')
        
        #处理内网
        if app['ip'].split('.')[0] in ['10','172']:
            inner_ip ='and inner_ip="%s"'%(app['ip'])
         
            count = db.count(sql+where+inner_ip)
            
            if count==None:
                print 'SQL Error:%s'% sql+where+inner_ip 
                return False
            count = count['count']
           
            try:
                temp_app['public_ip'] = db.get('select public_ip from assets where inner_ip="%s"'% app['ip'])['public_ip']
            except:
                pass
            if count==0:
                 temp_app['inner_ip'] = app['ip']
                 db.insert('app_info',**temp_app)
            else:
                db.update('app_info',where+inner_ip,**temp_app)
                
        else:
            import re
            if app['type']=='web':
                app['ip'] = app['ip'].replace('http://','').split('/')[0]
                p=r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'
                mo = re.search(p ,app['ip'])
                if not mo:
                    domain = app['ip'].replace('http://','').split('/')[0]
                    app['ip'] = db.get('select ip from domain where domain="%s"'% domain)['ip']
                    temp_app['domain'] = domain
            public_ip ='and (public_ip="%s") '%(app['ip'])
         
            count = db.count(sql+where+public_ip)
            if count==None:
                print 'SQL Error:%s'% sql+where+public_ip 
                return False
            count = count['count']
            
            if count==0:
                 temp_app['public_ip'] = app['ip']
                 db.insert('app_info',**temp_app)
            else:
                db.update('app_info',where+public_ip,**temp_app)
                            
                       
    def run(self):
        '''
        业务入口
        '''
        try:
            #资产就是资产吧 不做为一个应用出现了，运维管理的是资产服务器，也就是应用的公网
            #self.assets2appinfo()
            
            api_data = self.get_api_data()
            if api_data == None:return 
            
            db = Custom_MySQL(using='center_app')    
       
            game = db.get('select id from main_category where prefix="%s"' % self.game_code)
            
            main_category_id = game['id']               
            #获取区组信息
            for dist in  api_data['dists']:
                
                print '========'+dist['name']+'+'+dist['code']
                
                sql ='select id from  sub_category where main_category_id ='+str(main_category_id)+ ' and name="'+dist['name']+'"'
                sub_category_id = db.get(sql)['id']
                
                
                #将各区组不共用信息入数据库
                for app in dist['ips']:
                    self.insert_db(main_category_id,sub_category_id,self.platform,app)
                            
                #处理共用信息     
                #for app in api_data['global']:
                    
                    
 
            #更新资产id
            db.execute('update app_info as a left join assets as b on a.public_ip = b.public_ip set a.assets_id = b.id where a.public_ip is not NULL')                              
            db.execute('update app_info as a left join assets as b on a.inner_ip = b.inner_ip set a.assets_id = b.id where a.inner_ip is not NULL')                              
        
        except Exception as e:
            print e
            #exit()
        
        
        
        
                    

