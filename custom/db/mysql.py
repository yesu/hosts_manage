#coding=utf-8
'''
Created on 2011-8-28
@author: wuqichao
@copyright: $Id: custom_mysql.py 12565 2013-01-29 08:00:34Z wuqichao $
'''
import sys


try:
    import MySQLdb
    import MySQLdb.cursors
    from MySQLdb import  IntegrityError  as IntegrityError
    from MySQLdb import OperationalError as OperationalError
    from MySQLdb import DatabaseError as DatabaseError
    from MySQLdb import InternalError as InternalError
except ImportError:
    print >> sys.stderr,"""\

There was a problem importing Python modules(MySQLdb-python) required.
The error leading to this problem was:
%s Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:
%s
""" % (sys.exc_info(), sys.version)



__ALL__=['Custom_MySQL']

class Custom_MySQL() :
    '''
    service 基础类
    '''

    def __init__(self,using=''):
        """
        @param cursor_hander:数据库句柄
        """
        self.cursor = None
        self.cursor_hander = using
        self.connections = None
        
        if str(self.cursor_hander).rstrip() == '':
            print 'please write Custom_MySQL`s using param'
            exit(0)
        try:
            
            databases ={
                        'center_app':{'host':'115.29.227.10', 'user':'remote','password':'1q2w3e4r!@#$', 'database':'center_app','charset':'utf8','port':3306,'connect_timeout':50},
                        'log':{'host':'115.29.227.10', 'user':'remote','password':'1q2w3e4r!@#$', 'database':'logs','charset':'utf8','port':3306,'connect_timeout':50},
            }

            
            
            database = databases[self.cursor_hander]
            
            
            self.connections = MySQLdb.connect(database['host'],database['user'],database['password'],
                                               database['database'],charset = database['charset'],
                                               port = int(database['port']),connect_timeout = int(database['connect_timeout']));
            self.connections.ping(True)
            self.cursor = self.connections.cursor(MySQLdb.cursors.DictCursor)
           
            
        except MySQLdb.Error, e:
          
            err_info = "Error %d: %s" % (e.args[0],e.args[1])
            print err_info
            sys.exit(1)

    def ping(self):

        self.connections.ping(True)

    def close(self):
        try:
            if self.connections:
                self.connections.close()
        except:
            pass

    def __del__(self):
        try:
            if self.connections:
                self.connections.close()
        except:
            pass

            
    def _execute(self, cursor, query, parameters):

        try:
            return cursor.execute(query, parameters)
        except OperationalError:
            Exception("OperationalError for Custom_MySQL._execute() query")
            raise
        except IntegrityError:
            Exception("IntegrityError for Custom_MySQL._execute() query")
            raise
        except DatabaseError:
            Exception("IntegrityError for Custom_MySQL._execute() query")
            raise

        except InternalError:
            Exception("IntegrityError for Custom_MySQL._execute() query")
            raise

    def _execute_affected_rows(self, query, *parameters):
        """
        @return: 返回单个结果
        @param query:SQL语句
        @param parameters:SQL语句参数
        """
        try:
            self._execute(self.cursor,query, parameters)
            return self.cursor.rowcount

        except OperationalError:
            Exception("OperationalError for Custom_MySQL.execute() query")
            raise

    def execute(self, query, *parameters):
        """
        @return: 返回单个结果
        @param query:SQL语句
        @param parameters:SQL语句参数
        """
        try:
            self._execute(self.cursor,query, parameters)
            return self.cursor.lastrowid

        except OperationalError:
            Exception("OperationalError for Custom_MySQL.execute() query")
            raise


    def executemany(self, query, parameters):
        """
        @return: 返回单个结果
        @param query:SQL语句
        @param parameters:SQL语句参数
        """

        try:
            self.cursor.executemany(query, parameters)
            return self.cursor.lastrowid
        except OperationalError:
            Exception("OperationalError for Custom_MySQL.executemany() query")
            raise

    def query(self, query, *parameters):
        """
        @return: 返回一个list，多个结果。
        @param query:SQL语句
        @param parameters:SQL语句参数
        """
        try:
            self._execute(self.cursor,query, parameters)
            return self.cursor.fetchall()

        except OperationalError:
            Exception("OperationalError for Custom_MySQL.query() query")
            raise

    def get(self, query, *parameters):
        """
        @return: 返回单个结果
        @param query:SQL语句
        @param parameters:SQL语句参数
        """
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            print query
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def count(self,query, *parameters):
        """
        @return: 返回单个结果
        @param query:SQL语句
        @param parameters:SQL语句参数
        """
        try:
            self._execute(self.cursor,query, parameters)
            return self.cursor.fetchone()

        except OperationalError:
            Exception("OperationalError for Custom_MySQL.count() query")
            raise

    def insert(self,table,**datas):
        '''
        @param table:表名
        @param datas:｛字段：值｝
        '''
        return Insert(self,table)(**datas)

    def update(self,table,where,**datas):
        '''
        @param table:表名
        @param datas:｛字段：值｝
        '''
        return Update(self,table,where)(**datas)

    def delete(self,table,where):
        '''
        @param table:表名
        @param datas:｛字段：值｝
        '''
        return Delete(self,table,where)()

    def begin(self):
        if self.cursor is not None:
            self.cursor.execute('set autocommit =0;')

    def commit(self):
        if self.cursor is not None:
            try:
                self.cursor.execute('COMMIT;')
            except Exception,e:
                self.cursor.execute('ROLLBACK;')
                Exception("OperationalError for Custom_MySQL.commit() Error:%s",e)
                raise

    def rollback(self):
        if self.cursor is not None:
            try:
                self.cursor.execute('ROLLBACK;')
            except Exception,e:
                Exception("OperationalError for Custom_MySQL.rollback() Error:%s",e)
                raise



class Insert:

    def __init__(self,db,tablename):

        self.db=db
        self.tablename=tablename

    def __call__(self,**fileds):
        columns=fileds.keys()
        _prefix="".join(['INSERT INTO `',self.tablename,'`'])
        _fields=",".join(["".join(['`',column,'`']) for column in columns])
        _values=",".join(["%s" for i in range(len(columns))])
        _sql="".join([_prefix,"(",_fields,") VALUES (",_values,")"])
        _params=[fileds[key] for key in columns] 
        return self.db.execute(_sql,*tuple(_params))

class Update:

    def __init__(self,db,tablename,where):
        self.db=db
        self._tablename=tablename
        self._where=where


    def __call__(self,**fileds):
        if len(fileds)<1:
            raise OperationalError,"Must have unless 1 field to update"
        _params=[]
        _cols=[]

        for i in fileds.keys():
            _cols.append("".join(["`",i,'`','=%s']))

        for i in fileds.values():
            _params.append(i)

        _sql_slice=["UPDATE ",self._tablename," SET ",",".join(_cols)]
        if self._where:
            _sql_slice.append(" WHERE "+self._where)

        _sql="".join(_sql_slice)

        return self.db._execute_affected_rows(_sql,*_params)

class Delete:
    def __init__(self,db,tablename,where):
        self.db=db
        self._tablename=tablename
        self._where=where

    def __call__(self):

        _sql_slice=["DELETE FROM `",self._tablename,"`"]
        if self._where:
            _sql_slice.append(" WHERE "+self._where)

            _sql="".join(_sql_slice)

            return self.db._execute_affected_rows(_sql)

