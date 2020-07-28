# -*- coding:utf-8 -*-
import os
import xml.dom.minidom
from fontTools.ttLib import TTFont
import requests
import re
import json
import poxyadater
import UpdateAdater

#更新时间:20200324 更新内容:/kslive接口的两种模式

class wx():
    url=""
    inputdata=""
    def __init__(self,req):
        parameters = req.split('&')  # 每一行是一个字段
        url = None
        inputdata = None
        print(parameters)
        try:
            for nowstr in parameters:
                print(nowstr)
                key, val = nowstr.split('=')
                if key == "url":
                    self.url = val
                if key == "inputdata":
                    self.inputdata = val
        except Exception as e:
            pass
        self.geturl(self.url)
        rel=self.getkey(self.inputdata)
        bejs = {}
        bejs["url"] = self.url
        bejs["arr"] = self.arr
        bejs["key"] = rel
        rejs = json.dumps(bejs)
        result = rejs
        self.result=result
    def geturl(self,url):
        url="http://shark.douyucdn.cn/app/douyu/res/font/"+url+".woff"
        print(url)
        print("开始转化")
        r = requests.get(url)
        testdata = r.content
        filename="wofftmp.woff"
        with open(filename,"wb")as f:
            f.write(testdata)
        font = TTFont('./wofftmp.woff')
        font.saveXML('./wofftmp.xml')
        filename="wofftmp.xml"
        with open(filename,"r")as f:
            data=f.read()
        self.data=data
        self.getArr()
    def getArr(self):
        data=self.data
        standArr=["zero","one","two","three","four","five","six","seven","eight","nine"]
        arr=[]
        for i in range(1,11):
            pat='<GlyphID id="'+str(i)+'" name="(.*?)"/>'
            name=self.reget(data,pat)
            num=0
            for j in range(0,10):
                if name==standArr[j]:
                    num=j
            arr.append(num)
        print(arr)
        self.arr=arr
    def getkey(self,inkey):
        virkey=str(inkey)
        rel=""
        for i in range(0,len(virkey)):
            for j in range(0,len(self.arr)):
                if virkey[i]==str(self.arr[j]):
                    rel=rel+str(j)
        print(rel)
        return rel
    def reget(self,context,pat):
        cont = re.findall(pat, context)[0]
        return cont



# 返回码
class ErrorCode(object):
    OK = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"


# 将字典转成字符串
def dict2str(d):
    s = ''
    for i in d:
        s = s + i+': '+d[i]+'\r\n'
    return s

class Session(object):
    def __init__(self):
        self.data = dict()
        self.cook_file = None

    def getCookie(self, key):
        if key in self.data.keys():
            return self.data[key]
        return None

    def setCookie(self, key, value):
        self.data[key] = value

    def loadFromXML(self):
        import xml.dom.minidom as minidom
        root = minidom.parse(self.cook_file).documentElement
        for node in root.childNodes:
            if node.nodeName == '#text':
                continue
            else:
                self.setCookie(node.nodeName, node.childNodes[0].nodeValue)        

    def write2XML(self):
        import xml.dom.minidom as minidom
        dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'Root', None)
        root = dom.documentElement
        for key in self.data:
            node = dom.createElement(key)
            node.appendChild(dom.createTextNode(self.data[key]))
            root.appendChild(node)
        print(self.cook_file)
        with open(self.cook_file, 'w') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')

tts=0
class HttpRequest(object):
    RootDir = 'root'
    NotFoundHtml = RootDir+'/404.html'
    CookieDir = 'root/cookie/'
    sqlname = "./ksSpider/ks.db"
    s1 = None
    def __init__(self):
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.Cookie = None
        self.request_data = dict()
        self.response_line = ''
        self.response_head = dict()
        self.response_body = ''
        self.session = None
        # self.s1 = sqltest.SQLclass(self.sqlname)
        # self.slide=SlideProxy.slideproxy()
        self.updateAdater = UpdateAdater.updateadater()
        # print("调用HttpRequest构造函数")
        # self.appAdater.livesquare.ThreadStart()

    def passRequestLine(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url = header_list[1]
        if self.url == '/':
            self.url = '/index.html'
        self.protocol = header_list[2]

    def passRequestHead(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val
            # print key, val
        if 'Cookie' in self.head:
            self.Cookie = self.head['Cookie']
    def cutreq(self,req):
        argsArr = req.split("&")
        param = {}
        for args in argsArr:
            tmp = args.split("=")
            param[tmp[0]] = tmp[1]
        return  param


    def passRequest(self, request):
        request_byte=request
        request = request.decode('utf-8',errors='ignore')
        if len(request.split('\r\n', 1)) != 2:
            return
        postadata=b""
        try:
            postadata = request_byte.split(b'\r\n', 1)[1].split(b'\r\n\r\n', 1)[1]
        except Exception as e:
            # print("PostData Null")
            pass
        request_line, body = request.split('\r\n', 1)
        request_head = body.split('\r\n\r\n', 1)[0]     # 头部信息
        self.passRequestLine(request_line)
        self.passRequestHead(request_head)

        # 所有post视为动态请求
        # get如果带参数也视为动态请求
        # 不带参数的get视为静态请求
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            req = self.url.split('?', 1)[1]
            s_url = self.url.split('?', 1)[0]
            result=""
            if "updateadater" in s_url:
                result = self.updateAdater.adater(s_url,req,postadata)
            self.dynamicRequest(result)
        if self.method == 'GET':
            if self.url.find('?') != -1:        # 含有参数的get
                self.request_data = {}
                req = self.url.split('?', 1)[1]
                s_url = self.url.split('?', 1)[0]
                parameters = req.split('&')
                result=""
                if s_url == "/proxy":
                    p1 = poxyadater.poxynet()
                    result = p1.post(req)
                if "updateadater" in s_url:
                    result = self.updateAdater.adater(s_url,req,postadata)
                self.dynamicRequest(result)
            else:
                self.staticRequest(HttpRequest.RootDir + self.url)

    # 只提供制定类型的静态文件
    def staticRequest(self, path):
        print("调用了静态get")
        print(path)

        result=""
        self.dynamicRequest(result)

    def processSession(self):
        self.session = Session()
        # 没有提交cookie，创建cookie
        if self.Cookie is None:
            self.Cookie = self.generateCookie()
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            self.session.write2XML()
        else:            
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            if os.path.exists(cookie_file):
                self.session.loadFromXML()                
            # 当前cookie不存在，自动创建
            else:
                self.Cookie = self.generateCookie()
                cookie_file = self.CookieDir+self.Cookie
                self.session.cook_file = cookie_file
                self.session.write2XML()                
        return self.session


    def generateCookie(self):
        import time, hashlib
        cookie = str(int(round(time.time() * 1000)))
        hl = hashlib.md5()
        hl.update(cookie.encode(encoding='utf-8'))
        return cookie

    def dynamicRequest(self, path):
        # 如果找不到或者后缀名不是py则输出404
        # print(path)
        f = open(HttpRequest.NotFoundHtml, 'r')
        self.response_line = ErrorCode.OK
        self.response_head['Content-Type'] = 'text/html'
        self.response_body = path


    def getResponse(self):
        return self.response_line+dict2str(self.response_head)+'\r\n'+self.response_body
