import time
from pprint import pprint
from assets import assets
from custom.db.mysql import Custom_MySQL
from manage.mtask import Mtask
from manage.auto_run import auto_run

            
        
class last_ip(auto_run):
    
    
    def __init__(self):
        
        temp = []
        for i in assets.get_assets():
            i['cmd']  = '''ls|wc -l'''
            temp.append(i)
            
        super(last_ip, self).__init__(temp)
        
    def call_back(self,data=[]):
        
        db = Custom_MySQL(using='center_app')

        for result in data:

            if result !=[] and result['flag'] == '1':
                
                param = {}
                param['is_manage'] = 1
                db.update('assets', 'public_ip="%s"' %  result['ip'], **param)
                db.commit()
                
            else:
                print result
                param = {}
                param['is_manage'] = 0
                db.update('assets', 'public_ip="%s"' %  result['ip'], **param)
                db.commit()
                

if __name__ == '__main__':
    a =last_ip().start()
