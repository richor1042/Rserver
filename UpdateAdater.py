import HotUpdate
from urllib import parse
class updateadater():
    hotupadate=HotUpdate.hotupdate()
    def cutreq(self,req):
        argsArr = req.split("&")
        param = {}
        for args in argsArr:
            tmp = args.split("=")
            param[tmp[0]] = tmp[1]
        return  param
    def adater(self,url,req,postdata):
        rel=""
        if url=="/updateadater/GetVersion":
            #http://192.168.1.44:8000/updateadater/GetVersion?ID=132
            rel=self.hotupadate.GetVersion()
        if url=="/updateadater/UpdateFile":
            #http://192.168.1.44:8000/updateadater/UpdateFile?path=Hottest%2Ftst1
            rel=self.UpdateFile(req,postdata)
        return rel
    def UpdateFile(self,req,postdata):
        rel="Faild"
        param=self.cutreq(req)
        path=parse.unquote(param.pop('path',""))
        if path!="":
            rel=self.hotupadate.Update(path,postdata)
        # print("进来更新了啊")
        return rel
