# encoding=utf-8
from urllib import parse
import requests

import uuid

class poxynet():
    def cutreq(self,req):
        argsArr = req.split("&")
        param = {}
        for args in argsArr:
            tmp = args.split("=")
            param[tmp[0]] = tmp[1]
        return  param
    def post(self,req):
        #http://192.168.1.44:8000/proxy?url=https%3A%2F%2Fwww.baidu.com&isproxy=1
        print("开始代理")
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        }
        parm = self.cutreq(req)
        args={
            "url" : "",
            "isproxy":"0",
            "postdata":""
        }
        for key in parm:
            if key.find("head") > -1:
                headkey = key[4:]
                head[headkey] = parse.unquote(parm[key])
            else:
                args[key]=parse.unquote(parm[key])


        args["postdata"]=args["postdata"].replace('\r', '\\r').replace('\n', '\\n')
        print(args["url"])
        if args["url"].find("gifshow.com")>0:
            did="web_"+str(uuid.uuid1()).replace("-","")
            head["Cookie"]="did="+did
            print("自动添加did")

        print(args["postdata"])
        print(head)
        args["postdata"]=args["postdata"].encode()
        if args["isproxy"]=="1":
            tmppro = {'http': '120.210.219.73:8080'}
            tmpip='120.210.219.73:8080'
            # tmppro['http'] = tmpip
            # tmppro['https'] = tmpip

            print("代理ip"+tmppro['http'])
            try:
                if args["postdata"]==b"":
                    print("开始代理")
                    print(args["url"])
                    print(head)
                    print(tmppro)
                    r = requests.get(url=args["url"], headers=head, proxies=tmppro, timeout=20)
                else:
                    r = requests.post(url=args["url"], headers=head, data=args["postdata"], proxies=tmppro,timeout=20)
            except Exception as e:
                print("代理失败")
                return "代理失败"
        else:
            print(args["postdata"])
            if args["postdata"] == b"":
                # print("get请求")
                r = requests.get(url=args["url"], headers=head)
            else:
                r = requests.post(url=args["url"], headers=head, data=args["postdata"])
        testdata = r.content
        data = testdata.decode()

        return data
