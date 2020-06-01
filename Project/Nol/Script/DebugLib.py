#!/usr/bin/env python
# -*- coding : utf-8 -*-
# demo debug pjh

import mysql.connector
import os
import pandas as pd

#数据库操作
class Batch_db():
    @classmethod
    def login(
            cls,
            #配置连接
            DSN={
                'db_host':'10.129.35.109',
                'db_port':'4000',
                'db_usr':'root',
                'db_password':'spdb@nol0856',
                'db_name':'JIEB'
            },
            ENC='UTF-8'
    ):
        try:
            cls.cnxn = mysql.connector.connect(
                host=DSN.get('db_host'),
                port=DSN.get('db_port'),
                user=DSN.get('db_usr'),
                password=DSN.get('db_password'),
                database=DSN.get('db_name'),
                charset=ENC,
                connect_timeout=10,
                raise_on_warnings=True,
                use_pure=True)
        except Exception as ex:
            print('Error,Connect DB error:%s' % ex)
            cls.cnxn =None

    @classmethod
    def query(cls,statement,parameter=None,close=True):
        # print(statement,parameter)
        # if not self.cur():
        #     return False
        result = None

        cls.login()

        cur =cls.cnxn.cursor(dictionary=True)
        try:
            cur.execute(statement,parameter)
            result =cur.fetchall()
            #注释掉 数据过多
            #print.info(result)
        except Exception as ex:
            print('SQL_ERROR: %s,statement:%s' %(ex,statement))
        return result

    @classmethod
    def truncate(cls,**args):
        cls.login()
        result = None
        cur =cls.cnxn.cursor(dictionary=True)
        statement = 'truncate table %s' % args.get('tbname')
        try:
            cur.execute(statement)
            result = cur.fetchall()
            #注释掉，数据过多
            #print(result)
        except Exception as ex:
            print('SQL_ERROR: %s,statement:%s' %(ex,statement))
        return {
            'action':'truncate table %s'%args.get('tbname'),
            'result':'pass'
        }

    @classmethod
    def insert_sigle(cls, statement,parameter=None,**args):
        cls.login()
        result =None
        cur = cls.cnxn.cursor(dictionary=True)
        try:
            cur.executeemany(statement,parameter)
            cls.cnxn.commit()
        except Exception as ex:
            return {
                'action' :'insert sigle error:%s'%ex,
                'result' :'Fail'
            }
        return {
            'action': 'insert sigle succsessfully',
            'result': 'Pass'
        }

    @classmethod
    def insert_many(cls, statement,parameter=None,**args):
        cls.login()
        result =None
        cur = cls.cnxn.cursor(dictionary=True)
        try:
            cur.executeemany(statement,parameter)
            cls.cnxn.commit()
        except Exception as ex:
            return {
                'action' :'insert manydata error:%s'%ex,
                'result' :'Fail'
            }
        return {
            'action': 'insert manydata succsessfully',
            'result': 'Pass'
        }


'''
    n=cursor.execute(sql,param)
    我们要使用连接对象获得一个cursor对象,接下来,我们会使用cursor提供的方法来进行工作.
    这些方法包括两大类:1.执行命令,2.接收返回值
    cursor用来执行命令的方法:
　 callproc(self, procname, args):用来执行存储过程,接收的参数为存储过程名和参数列表,返回值为受影响的行数
　 execute(self, query, args):执行单条sql语句,接收的参数为sql语句本身和使用的参数列表,返回值为受影响的行数
　 cursor用来接收返回值的方法:
　 fetchall(self):接收全部的返回结果行.
'''
#导入文件操作
class Batch_csv():

    def __init__(self,file):
        csv_file = os.path.join('C:/Users/周易人/Desktop/Git/Project/Nol/bat_files/Jieb',file)

        if os.path.isfile(csv_file):
            self.df = pd.DataFrame(pd.read_csv(csv_file))
        else:
            self.df = None

    #排序
    def sort(self,file):
        self.df = self.df.sort_values(by=[],ascending=True)

    @property
    def tran_list(self):
        '''
        @property 将类的方法转化为类的属性，属性可以 df.tran_list使用，方法需要df.tran_list()
        转化字典输出
        :return: list of dict unit
        '''
        return self.df.to_dict(orient='records')

    @property
    def len(self):
        return len(self.df)

    @property
    def columns(self,):
        return list(self.df.columns.values)

    def getlines(self,):
        '''
        :return: 获取数据条数
        '''
        for i in range(len(self.df)):
            document = self.df[i:i+1]
            yield document

    def tran_dict(self):
        tran_list = self.tran_list
        dict1 = {}
        for i in tran_list:
            x =i.get('contract_no','err')

if __name__=='__main__':
        x  = Batch_db.query("select * from %s" %'tablename')
        b = Batch_csv('filename')





