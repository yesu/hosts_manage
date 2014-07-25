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
            
                
    def run(self):
        '''
        业务入口
        '''
        api_data = self.get_api_data()
        if api_data == None:return 
        
        db = Custom_MySQL(using='center_app')
        
        #更新大类中的应用类型
        app_type ={}
        app_type ={'app_type':','.join(api_data['type'])}
        db.update('main_category',' prefix="%s" ' % self.game_code,**app_type)
        
        
        game = db.get('select id from main_category where prefix="%s"' % self.game_code)
        main_category_id = game['id'] 
                      
        #获取区组信息
        for dist in  api_data['dists']:
            
            print '========'+dist['name']+'+'+dist['code']
            
            sql ='select count(id) as count from  sub_category where main_category_id ='+str(main_category_id)+ ' and name="'+dist['name']+'"'
            count = db.count(sql)
            if count==None:
                print 'SQL Error:%s'% sql 
                return False
            
            #区组更新内容
            dist_data ={}
            dist_data ={'prefix':dist['code'],
                        'main_category_id':main_category_id,
                        'name':dist['name'],
                        'platform':self.platform}
            
            #如果没有区组信息则保存  
            if count['count'] == 0:
                 db.insert('sub_category',**dist_data)
            else:
                 db.update('sub_category',' main_category_id ='+str(main_category_id)+ ' and name="'+dist['name']+'"',**dist_data)

             
                    

