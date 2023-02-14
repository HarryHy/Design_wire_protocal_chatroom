import socket
import threading
import queue
import json 
import os
import os.path
import sys

IP = '127.0.0.1'
PORT = 9999 # 端口
messages = queue.Queue()
lock = threading.Lock()
users = []
total_users = []

def onlines(): # 统计当前在线人员
    online = []
    for i in range(len(users)):
        online.append(users[i][0])
    return online

class ChatServer(threading.Thread):
    global users, que, lock, total_users

    def __init__(self): # 构造函数
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        os.chdir(sys.path[0])
    
    def run(self):
        self.s.bind((IP,PORT))
        self.s.listen(5)
        q = threading.Thread(target=self.sendData)
        q.start()
        try:
            while True:
                #connect with the client
                conn, addr = self.s.accept()
                t = threading.Thread(target=self.receive, args=(conn, addr))
                t.start()
            self.s.close()
        except:
            self.s.close()
    
    def sendData(self): # 发送数据
        while True:
            if not messages.empty():
                try:
                    message = messages.get()
                    print("get the message 1")
                    if isinstance(message[1], str):
                        for i in range(len(users)):
                            data = ' ' + message[1]
                            users[i][1].send(data.encode())
                            print(data)
                            print('\n')
                except Exception as e:
                    print("send Data error 1")
                    print(e)
                    pass

                if isinstance(message[1], list):
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            users[i][1].send(data.encode())
                        except:
                            print("send Data error 2")
                            pass

    def Load(self, data, addr):
        lock.acquire()
        try:
            messages.put((addr, data))
        finally:
            lock.release() 

    def receive(self, conn, addr): # 接收消息
        user = conn.recv(1024) # 用户名称
        user = user.decode()
        if user == '用户名不存在':
            user = addr[0] + ':' + str(addr[1])
        tag = 1
        temp = user

        for i in range(len(users)): # 检验重名，则在重名用户后加数字
            if users[i][0] == user:
                tag = tag + 1
                user = temp + str(tag)
        users.append((user, conn))
        USERS = onlines()
        self.Load(USERS,addr)

        # 在获取用户名后便会不断地接受用户端发来的消息（即聊天内容），结束后关闭连接。
        try:
            while True:
                message = conn.recv(1024) # 发送消息
                message = message.decode()
                message = user + ':' + message
                self.Load(message,addr)
            conn.close()
# 如果用户断开连接，将该用户从用户列表中删除，然后更新用户列表。
        except:
            j = 0 # 用户断开连接
            for man in users:
                if man[0] == user:
                    users.pop(j) # 服务器段删除退出的用户
                break
            j = j+1
            USERS = onlines()
            self.Load(USERS,addr)
            conn.close()

if __name__ == '__main__':
    cserver = ChatServer()
    cserver.start()