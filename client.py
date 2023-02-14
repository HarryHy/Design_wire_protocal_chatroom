import socket
import tkinter
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
IP = ''
PORT = ''
user = ''
listbox1 = '' # 用于显示在线用户的列表框
show = 1 # 用于判断是开还是关闭列表框
users = [] # 在线用户列表
chat = '------Group chat-------' # 聊天对象

root0 = tkinter.Tk()
root0.geometry("300x250")
root0.title('logging in')
root0.resizable(0,0)
one = tkinter.Label(root0,width=300,height=250,bg="LightBlue")
one.pack()

IP0 = tkinter.StringVar()
IP0.set('127.0.0.1')
USER = tkinter.StringVar()
USER.set('username')
PORT0 = tkinter.StringVar()
PORT0.set('9999')

labelIP = tkinter.Label(root0,text='IP Address : Port',bg="LightBlue")
labelIP.place(x=20,y=20,width=100,height=40)

entryIP = tkinter.Entry(root0, width=60, textvariable=IP0)
entryIP.place(x=120,y=25,width=100,height=30)

labelUSER = tkinter.Label(root0,text='USERNAME',bg="LightBlue")
labelUSER.place(x=20,y=70,width=100,height=40)

entryUSER = tkinter.Entry(root0, width=60, textvariable=USER)
entryUSER.place(x=120,y=75,width=100,height=30)


labelPORT = tkinter.Label(root0,text='PORT',bg="LightBlue")
labelPORT.place(x=20,y=120,width=100,height=40)

entryPORT = tkinter.Entry(root0, width=60, textvariable=PORT)
entryPORT.place(x=120,y=125,width=100,height=30)

def Login(*args):
    global IP, PORT, user
    IP= entryIP.get()
    user = entryUSER.get()
    PORT =  entryPORT.get()

    if not user:
        tkinter.messagebox.showwarning('warning', message='USERNAME is EMPTY')
    else:
        root0.destroy()

loginButton = tkinter.Button(root0, text ="Sign in", command = Login,bg="Yellow")
loginButton.place(x=135,y=200,width=40,height=25)
root0.bind('<Return>', Login)
root0.mainloop()

# 建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, int(PORT)))
if user:
    s.send(user.encode()) # 发送用户名
else:
    s.send('用户名不存在'.encode())
    user = IP + ':' + PORT

# 聊天窗口
root1 = tkinter.Tk()
root1.geometry("640x480")
root1.title('群聊')
root1.resizable(0,0)

listbox = ScrolledText(root1)
listbox.place(x=0, y=0, width=1280, height=320)
listbox.tag_config('tag1', foreground='red',backgroun="yellow")
listbox.insert(tkinter.END, 'welcome to the chatroom\n', 'tag1')
listbox.insert(tkinter.END, "To send private message, \n please use \"message sender ~ receiver\" formate ", 'tag1')
INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(root1, width=120, textvariable=INPUT)
entryIuput.place(x=5,y=320,width=480,height=170)

# 在线用户列表
listbox1 = tkinter.Listbox(root1)
listbox1.place(x=420, y=0, width=400, height=320)

def send(*args):
    message = entryIuput.get() + '~' + user + '~' + chat
    s.send(message.encode())
    INPUT.set('')

sendButton = tkinter.Button(root1, text ="\n SEND \n ",anchor = 'n',command =
send,font=('Helvetica', 18),bg = 'white')
sendButton.place(x=585,y=320,width=55,height=300)
root1.bind('<Return>', send)

def receive():
    global uses
    try:
        while True:
            data = s.recv(1024)
            data = data.decode()
            print(data)
            try:
                uses = json.loads(data)
                listbox1.delete(0, tkinter.END)
                listbox1.insert(tkinter.END, "当前在线用户")
                #listbox1.tag_config('tag5', foreground='yellow')
                listbox1.insert(tkinter.END, "My user name is :" + str(user))
                listbox1.insert(tkinter.END, "------Online User List-------")
                for x in range(len(uses)):
                    listbox1.insert(tkinter.END, uses[x])
                users.append('------Group chat-------')
            except:
                try:
                    data = data.split('~')
                    message = data[0]
                    userName = data[1]
                    chatwith = data[2]
                    message = '\n' + message
                    if chatwith == '------Group chat-------': # 群聊
                        if userName == user:
                            listbox.insert(tkinter.END, message)
                        else:
                            listbox.insert(tkinter.END, message)
                    elif userName == user or chatwith == user: # 私聊
                        if userName == user:
                            listbox.tag_config('tag2', foreground='red')
                            listbox.insert(tkinter.END, message, 'tag2')
                        else:
                            listbox.tag_config('tag3', foreground='green')
                            listbox.insert(tkinter.END, message,'tag3')
                    
                    listbox.see(tkinter.END)
                except Exception as e:
                    print(e)
                    print("incorrect usage")
                    pass
    except:
        print("end of using")
r = threading.Thread(target=receive)
r.start() # 开始线程接收信息
root1.mainloop()
s.close()