import HotUpdate
import re
class startupdate():
    hotupadate=HotUpdate.hotupdate()
    filename="版本信息.txt"
    def ReadIps(self):
        with open(self.filename,"r")as f:
            tmp=f.read()
        pat="目标IP:(.*?)\n"
        cont=re.findall(pat,tmp)
        rel=[]
        if len(cont)>0:
            ips=cont[0]
            rel=ips.split("/")
        # print(rel)
        return rel
    def Start(self):
        ips=self.ReadIps()
        if ips==[]:
            print("目标服务器为空")
            return
        for ip in ips:
            self.hotupadate.CheckUpdateFile(ip)

su=startupdate()
su.Start()
