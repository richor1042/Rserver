# -*- coding=utf-8 -*-
import socket
import threading
import queue
from HttpHead import HttpRequest
import _thread
import time
import re





# 每个任务线程
class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 线程池
class ThreadPoolManger():
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):     # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


def tcp_link(sock, addr):
    print('Accept new connection from %s:%s...' % addr)

    bb=True
    tmprequest = sock.recv(10240)
    request=tmprequest
    pat=b"Content-Length: (.*?)\r"
    Content_Length=0
    try:
        cont=re.findall(pat,request)
        tmplen=cont[0]
        tmpint=tmplen.decode()
        Content_Length=int(tmpint)
    except Exception as e:
        pass

    while len(request)<Content_Length:
        tmprequest = sock.recv(10240)
        request=request+tmprequest



    http_req = HttpRequest()
    http_req.passRequest(request)
    try:
        sock.send(http_req.getResponse().encode('utf-8'))
    except Exception as e:
        print(e)
    sock.close()


def start_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(30)
    thread_pool = ThreadPoolManger(5)
    print('listen in %s:%d' % ('0.0.0.0', port))
    print("version:20200522")
    while True:
        sock, addr = s.accept()
        thread_pool.add_work(tcp_link, *(sock, addr))



if __name__ == '__main__':
    for i in range(8000,8001):
        _thread.start_new_thread(start_server,(i,))
    while True:
        time.sleep(1000)
    # start_server(9999)
    pass

