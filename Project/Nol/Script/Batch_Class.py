#!/usr/bin/env python
# -*- coding : utf-8 -*-
# demo debug pjh

import sys
import os
import json
import re
import time
import decimal
import traceback
import imaplib
import paramiko
import requests

from Script.ras_Encrypt import Encrypt
#添加路径,用于调用模块,以及putfile方法调用的localpath
sys.path.append('C:/Users/周易人/Desktop/Git/Project/Nol/Script')

class Batch_File():
    #实例化
    def __init__(self):
        pass

    @classmethod
    def cleanup(cls,**args):
        #from nol project
        args.update(
            {'ip':'10.137.18.44',
            'port':'22',
            'username':'nol',
            'password':'Nol12345'
            }
        )
        ip = args.get('ip')
        port = int(args.get('port',22))
        username = args.get('username','root')
        password = args.get('password','root')
        #remotepath 为被清空标文件在18.44的绝对路径
        remotepath = args.get("remotepath")

        client = paramiko.SSHClient()#ssh连接
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())#允许连接know_hosts中不存在的主机
        client.connect(hostname=ip,port=int(port),username=username,)
        '''
        linux中stdin，stdout和stderr，这3个可以称为终端Terminal的
        标准输入standard input，标准输出standard out和标准错误输出standard error 
        '''
        stdin, stdout, stderr = client.exec_command('rm %s' %remotepath ,timeout=60)#执行linux rm指令
        return {
            'action' : 'rm remotefile {0}'.format(remotepath),
            'result' : 'pass'
        }

    @classmethod
    def putfile(cls,**args):
        args.update(
            {'ip':'10.137.18.44',
            'port':'22',
            'username':'nol',
            'password':'Nol12345'
            }
        )
        ip = args.get('ip')
        port = int(args.get('port',22))
        username = args.get('username','root')
        password = args.get('password','root')

        tran = paramiko.transport((ip,port))#文件上传的方法
        localpath = args.get('localpath')
        remotepath = args.get('remotepath')

        localpath2 =os.path.join('/zdhapp/project_git/NOL',localpath)

        if not os.path.isfile(localpath2):
            return {
                'action':'{0} is not exist'.format(localpath),
                'result':'Failed'
            }
        #连接SSH服务端，使用password
        tran.connect(username=username,password=password)
        #获取SFTP实例
        sftp = paramiko.SFTPClient.from_transport(tran)
        #执行上传动作
        sftp.put(localpath2,remotepath)
        print('put file {0} to {1} '.format(localpath,remotepath))
        return {
            'action':'put file {0} to {1} '.format(localpath,remotepath),
            'result':'pass'
        }

    @classmethod
    def getfile(cls,**args):
        args.update(
            {'ip':'10.137.18.44',
            'port':'22',
            'username':'nol',
            'password':'Nol12345'
            }
        )
        ip = args.get('ip')
        port = int(args.get('port',22))
        username = args.get('username','root')
        password = args.get('password','root')
        tran = paramiko.transport((ip, port))
        localpath = args.get('localpath')
        remotepath = args.get('remotepath')
        #连接SSH服务端，使用password
        tran.connect(username=username,password=password)
        #获取SFTP实例
        sftp = paramiko.SFTPClient.from_transport(tran)
        #设置上传的本地/远程文件路径
        #执行下载动作
        localpath2 = os.path.join('/zdhapp/project_git/NOL', localpath)
        sftp.get(remotepath,localpath2)
        print('get remotefile from {0},localfile : {1}'.format(remotepath,localpath2))
        return {
            'action':'get remotefile from {0},localfile : {1}'.format(remotepath,localpath2),
            'result':'pass'
        }


class PL_NOL():
    def __init__(self):
        pass

    @classmethod
    def login(cls):
        cls.addr = 'http://10.137.18.44:4455'
        cls.proxies = {'http':'10.129.53.74:8888','https':'10.129.53.74:8888'}#代理ip，https为新增数据加密版本的http通讯协议
        cls.proxies = {'http':None,'https':None}

        cls.sess = requests.session()#cookie数据存放在客户的浏览器上，session数据放在服务器上

        loginkey_header = {
            'Accept':'pplication/json, text/plain, */*'
        }
        try:
            '''
            Accept这个字段是用来通知服务器，
            用户代理（浏览器等客户端）能够处理的媒体类型及媒体类型的相对优先级。           
            '''
            res = cls.sess.get(cls.addr + '/DemoMaster/login/key',
                               headers = loginkey_header,
                               timeout =(120,120),
                               proxies =cls.proxies,
                               verify = False,allow_redirects =True)#避免ssl认证并启动重定向
        except Exception as ex:
            print('error : {0}'.format(ex))

        else:
            if res.json() !='' and res.json() !={}:
                username = 'admin'
                password_msg = 'admin'

                key = res.json()
                en = Encrypt(exponent = key['exponent'],modulus = key['modulus'])
                password =en.encrypt(password_msg)

                login_data = 'username={0}&password={1}'.format(username,password)\

                my_header ={
                    'Content-Type':'application/x-www-form-urlencoded',
                    'Accept':'pplocation/json, text/plain, */*'
                }

                try:
                    rsp = cls.sess.post(cls.addr+'/DemoMaster/login',
                                        headers=loginkey_header,
                                        timeout=(120, 120),
                                        proxies=cls.proxies,
                                        verify=False, allow_redirects=True)  # 避免ssl认证并启动重定向
                    print(rsp.text)
                except Exception as ex:
                    print('error:{0}'.format(ex))
                else:
                    if rsp.text !='':
                        print('error:{0}'.format(rsp.text))
                        cls.sess =None
            else:
                print(res.json())
                cls.sess =None

    @classmethod
    def logout(cls):
        cls.sess = requests.session()

        cls.sess.get(url=cls.addr +'/DemoMaster/logout',proxies=cls.proxies,verify=False)

    @classmethod
    def runjob(cls,**args):
        pass
        #
        # res = ''
        # rtmsg =dict()
        #
        # cls.login()
        #
        # if cls.sess is None:
        #     rtmsg['result'] = 'Failed'
        #     rtmsg['action'] = '用户登陆失败'
        #     return rtmsg
        # rundata ={
        #     'jobName' :args.pop('jobname'),
        #     'key':','.join(args.keys()),
        #     'values':','.join(args.values())
        # }
        # my_header = {
        #     'Content-Type':'application/x-www-form-urlencoded',
        #     'Accept':'pplication/json,text/plain,*/*'
        # }
        #
        # try:
        #     rsp = cls.sess.post(cls.addr + '/DemoMaster/batch/launch',
        #                         headers=rundata,
        #                         timeout=(120, 120),
        #                         proxies=cls.proxies,
        #                         verify=False, allow_redirects=True)  # 避免ssl认证并启动重定向
        #
        #
        #


