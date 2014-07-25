from custom.db.mysql import Custom_MySQL
from yun.dns import dns

if __name__ == '__main__':
        
        db = Custom_MySQL(using='center_app')
        d = dns()
        domains = d.get_result()
        #print domains
        for k,v in domains.items():
            print k
            data ={}
            data= {'ip':v,'domain':k}
            sql ='select count(*) as count from domain where domain="%s"'%k
            if db.count(sql)['count'] == 0:
                db.insert('domain',**data)
                db.commit()