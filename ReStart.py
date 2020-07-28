#!/usr/bin/evn python
# -*- coding:utf-8 -*-
import subprocess, time, sys

TIME = 600  # 程序状态检测间隔（单位：秒）
CMD = "server.py"  # 需要执行程序的绝对路径，支持jar 如：D:\\calc.exe 或者D:\\test.jar


class Auto_Run():
    def __init__(self, sleep_time, cmd):
        self.sleep_time = sleep_time
        self.cmd = cmd
        self.ext = (cmd[-3:]).lower()  # 判断文件的后缀名，全部换成小写
        self.p = None  # self.p为subprocess.Popen()的返回值，初始化为None
        self.run()  # 启动时先执行一次程序
        self.filename="IsUpating.txt"

        try:
            while 1:
                # time.sleep(sleep_time)
                # stat="1"
                # while stat=="1":
                #     with open(self.filename,"r")as f:
                #         stat=f.read()
                #     time.sleep(1)
                tt=0
                while tt<sleep_time:
                    time.sleep(1)
                    with open(self.filename,"r")as f:
                        stat=f.read()
                    if stat!="1":
                        tt=tt+1
                    if stat=="2":
                        tt=sleep_time
                        with open(self.filename,"w")as f:
                            f.write("0")
                        print("接收到更新文件,强制重启")
                self.poll = self.p.poll()  # 判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出
                if self.poll is None:
                    print(u"准备自动重启程序")
                    self.p.kill()
                    time.sleep(1)
                    self.run()
                else:
                    print(u"未检测到程序运行状态，准备启动程序")
                    self.run()
        except KeyboardInterrupt as e:
            print(u"检测到CTRL+C，准备退出程序!")
            self.p.kill()  # 检测到CTRL+C时，kill掉CMD中启动的exe或者jar程序

    def run(self):
        self.p = subprocess.Popen(['python','%s' % self.cmd], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
                                  shell=False)


app = Auto_Run(TIME, CMD)