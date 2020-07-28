import os
import re
import requests
from urllib import parse
import time
class hotupdate():
    filename="版本信息.txt"
    def GetCont(self,name,data):
        pat=name+"(.*?)\n"
        cont=re.findall(pat,data)
        # print(cont)
        rel=""
        if len(cont)>0:
            rel=cont[0]
        return rel
    def check_file(self,file_path):
        all_file = os.listdir(file_path)
        files = []
        for f in all_file:
            # print(f)
            if os.path.isdir(f):
                files.extend(self.check_file( file_path+'\\' + f))
            else:
                fsize=os.path.getsize(file_path+'\\' + f)
                # print(fsize)
                files.append(file_path+'\\'+ f+"_"+str(fsize))
        return files
    def GetDirData(self):
        rel=str(self.check_file("."))
        print(rel)
        return rel
    def DownFile(self,FileName):
        with open(FileName,"rb")as f:
            tmp=f.read()
        print(tmp)
        return tmp
    def GetVersion(self):
        with open(self.filename,"r")as f:
            tmp=f.read()
        # print(tmp)
        pat="Now Version:(.*?)\n"
        Now_Version=re.findall(pat,tmp)[0]
        print(Now_Version)
        return Now_Version
    def Update(self,path,ByteData):
        rel="sucess"
        try:
            loc=path.rfind("/")
            if loc>0:
                tmppath=path[:loc]
                if not os.path.exists(tmppath):
                    os.makedirs(tmppath)
            with open(path,"wb")as f:
                f.write(ByteData)
            print("写入成功")
        except Exception as e:
            print("更新"+path+"失败")
            print(e)
            rel="Faild"
        return rel
    def GetServerVersion(self,ip):
        url="http://"+ip+":8000/updateadater/GetVersion?ID=132"
        rel=""
        try:
            r=requests.get(url)
            testdata=r.content
            rel=testdata.decode()
        except Exception as e:
            pass
        return rel
    def ServerLock(self,ip,stat):
        bb=False
        print("开始更改"+ip+"服务器重启进程")
        url="http://"+ip+":8000/updateadater/UpdateFile?path=IsUpating.txt"
        postdata=stat
        xdata=""
        try:
            r=requests.post(url,postdata)
            testdata=r.content
            xdata=testdata.decode()
        except Exception as e:
            pass
        if xdata=="sucess":
            bb=True
            if stat=="1":
                print("服务器锁定成功")
            else:
                print("服务器解锁成功")
        return bb
    def UpateServerFile(self,path,ip):
        with open(path,"rb")as f:
            postdata=f.read()
        url="http://"+ip+":8000/updateadater/UpdateFile?path="+parse.quote(path)
        i=0
        xdata = ""
        while i<10 and xdata!="sucess":
            print("开始更新"+path)
            try:
                r = requests.post(url, postdata)
                testdata = r.content
                xdata = testdata.decode()
            except Exception as e:
                pass
        if xdata=="sucess":
            print("更新成功")
        else:
            print("更新失败")
            while 1==1:
                time.sleep(1)




    def CheckUpdateFile(self,ip):
        with open(self.filename,"r")as f:
            tmp=f.read()
        tmparr=tmp.split("--------------------------------------------------------")
        startVersion=self.GetServerVersion(ip)
        if startVersion=="":
            print("无法获取"+ip+"版本号，请检查服务端是否正常")
            return
        print(startVersion)
        # print("-------------")
        filearr=[]
        bb=False
        for i in range(1,len(tmparr)):
            if len(tmparr[i])>10:
                version=self.GetCont("版本号:",tmparr[i])
                filestr = self.GetCont("文件:", tmparr[i])
                # print(version)
                # print(filestr)
                # print("----------------------")
                if bb:
                    files=filestr.split(",")
                    for tmpfile in files:
                        if not(tmpfile in filearr):
                            filearr.append(tmpfile)
                if version==startVersion:
                    bb=True
        print("当前版本"+startVersion)
        print("升级文件：")
        print(filearr)
        if filearr==[]:
            print(ip+"版本已是最新")
            return
        self.ServerLock(ip,"1")
        for path in filearr:
            self.UpateServerFile(path,ip)
        self.UpateServerFile('版本信息.txt', ip)
        self.ServerLock(ip, "2")
        print("服务器"+ip+"升级成功")





# os.chdir('.\\KsData\\raw_data')
# hu=hotupdate()
# hu.ServerLock("47.100.246.73","2")
# hu.CheckUpdateFile("192.168.1.202")
# hu.GetDirData()
# hu.DownFile('.\\ADSLtest.py')
# hu.GetVersion()
# hu.Update("Hottest/Hottest8/Hottest9/tst3.txt",b"11111111111111")
# hu.CheckUpdateFile()