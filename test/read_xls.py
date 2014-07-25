# -*- coding: utf-8 -*- 
import  xdrlib ,sys
import xlrd
from custom.db.mysql import Custom_MySQL

def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    
    for rownum in range(1,nrows):

         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                 '''
                 if i == 0:
                     sql ='select count(*) as count from main_category where prefix= %s'
                     p =(row[i].split('_')[0],)
                     result= db.count(sql,*p)
                          
                     if result['count'] == 0:
                        param={}
                        print row[i].split('_')[0]
                        param['prefix']=row[i].split('_')[0]
                        param['name']=row[i].split('_')[0]
			db.insert('main_category',**param)
                        db.commit()
                 '''
                 app[colnames[i]] = row[i] 
             list.append(app)
    return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数 
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

def main():
   tables = excel_table_byindex()
   
   db = Custom_MySQL(using='center_app')
   
   for row in tables:
       if row['pub'] != "":
           param ={}
           param['pwd'] = row['pwd']
           db.update('assets','public_ip="%s"'%row['pub'],**param)
               
 


if __name__=="__main__":
    main()
