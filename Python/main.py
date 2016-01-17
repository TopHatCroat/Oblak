from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter.messagebox as tm
import socket
import re
# import sys
import os
import ntpath

HOST = 'localhost'
PORT = 4444
uploaded_files = []
feedback = []
link = ''
global user

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def refresh():
    global uploaded_files
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send('ref'.encode('utf-8'))
    #string = commandName.split(' ', 1)
    #inputFile = string[1]
    while True:
        data = socket1.recv(1024).decode('utf-8')
        if not data:
            break
        uploaded_files.append(data)
        #print(data.decode('utf-8'))
    #print ('REFRESH Successful')
    feedback = socket1.recv(1024).decode('utf-8')
    socket1.close()
    print(feedback)
    #print(uploaded_files)
    return

def upload(commandName, root):
    global feedback
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName.encode('utf-8'))
    string = commandName.split(' ', 1)
    #os.path.abspath(string[1].strip())
    #inputFile = path_leaf(string[1].strip())
    inputFile = string[1].strip()
    print(inputFile)
    with open(inputFile, 'r') as file_to_send:
        for data in file_to_send:
            socket1.sendall(data.encode('utf-8'))
    #print ('PUT Successful')
    feedback1 = socket1.recv(1024).decode('utf-8')
    socket1.close()
    print(feedback)
    feedback.append(feedback1)
    text_area(root)
    return


def download(commandName, root):
    global feedback
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName.encode('utf-8'))
    string = commandName.split(' ', 1)
    # string2 = ''.join(string[1])
    # if(string2[:1] == '!'):
    #     inputFile = string2.split('!', 1)
    #     inputFile = inputFile[1]
    # else:
    #     inputFile = string2
    # print('ftw%s' %inputFile)

    curpath = os.path.abspath(os.curdir)
    reqFile = path_leaf(string[1].strip())
    inputFile = os.path.join(curpath, reqFile)
    with open(inputFile, 'w') as file_to_write:
        while True:
            data = socket1.recv(1024)
            if not data:
                break
            file_to_write.write(data.decode('utf-8'))
    file_to_write.close()
    #print ('GET Successful')
    feedback1 = socket1.recv(1024).decode('utf-8')
    socket1.close()
    print(feedback)
    feedback.append(feedback1)
    text_area(root)
    return

def remove(commandName, root):
    global feedback
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName.encode('utf-8'))
    #print("command name %s" %commandName)
    string = commandName.split(' ', 1)
    #os.path.abspath(string[1].strip())
    #inputFile = path_leaf(string[1].strip())
    inputFile = string[1].strip()
    print(inputFile)
    # with open(inputFile, 'r') as file_to_send:
    #     for data in file_to_send:
    #socket1.send(inputFile.encode('utf-8'))
    #print ('PUT Successful')
    feedback1 = socket1.recv(1024).decode('utf-8')
    socket1.close()
    print(feedback)
    feedback.append(feedback1)
    text_area(root)
    return

def share(commandName, root):
    global link
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName.encode('utf-8'))
    #print("command name %s" %commandName)
    string = commandName.split(' ', 1)
    #os.path.abspath(string[1].strip())
    #inputFile = path_leaf(string[1].strip())
    inputFile = string[1]
    print(inputFile)
    # with open(inputFile, 'r') as file_to_send:
    #     for data in file_to_send:
    #socket1.send(inputFile.encode('utf-8'))
    #print ('PUT Successful')
    feedback = socket1.recv(1024).decode('utf-8')
    link += feedback
    print(link)
    socket1.close()
    return


# def register():
#     username = input('Enter your username: ')
#     password = input('Enter your password: ')
#     data= 'reg' + ' ' + username + ';' + password
#     socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     socket1.connect((HOST, PORT))
#     socket1.sendall(data.encode('utf-8'))
#     #socket1.close()
#     feedback = socket1.recv(1024)
#     print(feedback.decode('utf-8'))
#     socket1.close()
#     return

# def login():
#     username = input('Enter your username: ')
#     password = input('Enter your password: ')
#     data= 'log' + ' ' + username + ';' + password
#     socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     socket1.connect((HOST, PORT))
#     socket1.sendall(data.encode('utf-8'))
#     #socket1.close()
#     feedback = socket1.recv(1024)
#     print(feedback.decode('utf-8'))
#     socket1.close()
#     return

#*****************************GUI *************************************
def upload_button(root):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
    if filename != '':
        path = 'put' + ' ' + filename #Put do datoteke na PC-u
        upload(path, root)
    #print (path)
    area(root)

def download_button(root):
    downloadframe = Tk()
    downloadframe.title("Download")
    lb_1 = Label(downloadframe, text = "Filename")
    lb_1.grid(row = 0, column = 0, sticky = E)
    entry_1 = Entry(downloadframe)
    entry_1.grid(row = 0, column = 1)
    dbtn = Button(downloadframe, text = "Download", command = lambda : downloadfile(entry_1, root))
    dbtn.grid(columnspan = 2)

def downloadfile(entry_1, root):
    unos1 = entry_1.get()
    if unos1 != '':
        path = 'get' + ' ' + unos1
        download(path, root)

def remove_button(root):
    removeframe = Tk()
    removeframe.title("Remove file")
    lb_1 = Label(removeframe, text = "Filename")
    lb_1.grid(row = 0, column = 0, sticky = E)
    entry_1 = Entry(removeframe)
    entry_1.grid(row = 0, column = 1)
    dbtn = Button(removeframe, text = "Remove", command = lambda : removefile(entry_1, root))
    dbtn.grid(columnspan = 2)


def removefile(entry_1, root):
    unos1 = entry_1.get()
    if unos1 != '':
        path = 'rem' + ' ' + unos1
        remove(path, root)
    area(root)

def logout_button(root):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send('out'.encode('utf-8'))
    socket1.close()
    root.destroy()
    login()


def area(root):  #OVO COPY PASTE
    global uploaded_files
    area = Text(root)
    area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
    refresh()
    #area = Label(frame, text = '')
    for i in range (len(uploaded_files)):
        print(uploaded_files[i])
        area.insert(END, uploaded_files[i] + "\n")
    area.config(state=DISABLED)
    uploaded_files[:] = []

def text_area(root): #OVO COPY/PASTE
    global feedback
    var = feedback
    textarea = Label(root, text = var)
    textarea.grid(row = 5, column = 0, columnspan = 2, rowspan = 2, padx = 4, sticky = W + N)
    feedback[:] = []

def share_button(root):
    shareframe = Tk()
    shareframe.title("Share")
    lb_1 = Label(shareframe, text = "Filename")
    lb_1.grid(row = 0, column = 0, sticky = E)
    entry_1 = Entry(shareframe)
    entry_1.grid(row = 0, column = 1)
    dbtn = Button(shareframe, text = "Share", command = lambda : sharelink_(entry_1, root, shareframe))
    dbtn.grid(columnspan = 2)


def sharelink_(entry_1, root, shareframe):
    global link
    sharelink = Tk()
    sharelink.title("Share")
    unos = entry_1.get()
    shareframe.destroy()
    lb_1 = Label(sharelink, text = "Link:")
    lb_1.grid(row = 0, column = 0, sticky = E)
    data = 'shr' + ' ' + unos
    share(data, root)
    text = Text(sharelink, height = 1, width = 100)
    text.insert(END, link)
    text.grid(row = 0, column = 1)
    text.config(state = DISABLED)


def init():
    # frame = Frame(root)
    root = Tk()
    root.title("Projekt Oblak - %s" %user)
    root.geometry('{}x{}'.format(360, 240))
    root.columnconfigure(1, weight=1)
    root.columnconfigure(3, pad = 7)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, pad=7)

    lbl = Label(root, text="Files")
    lbl.grid(sticky=W, pady=4, padx=5,row = 0)

    # rbtn = Button(root, text = "REFRESH", command = lambda : area (root))
    # rbtn.grid(row = 4, column = 3)

    #area = Text(root)
    # area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
    # refresh()
    # for i in range (len(uploaded_files)):
    #     print(uploaded_files[i])
    #     area.insert(END, uploaded_files[i] + "\n")
    #area.config(state=DISABLED)

    # var = "asadakfjdal"
    # textarea = Label(root, text = var)
    # textarea.grid(row = 5, column = 0, columnspan = 2, rowspan = 2, padx = 4, sticky = W + N)
    area(root) #OVO COPY/PASTE
    text_area(root) #OVO COPY/PASTE

    ubtn = Button(root, text = "UPLOAD", command = lambda : upload_button(root))
    ubtn.grid(row = 1, column = 3)
    sbtn = Button(root, text = "DOWNLOAD", command = lambda : download_button(root))
    sbtn.grid(row = 2, column = 3)
    dbtn = Button(root, text = "DELETE", command = lambda : remove_button(root))
    dbtn.grid(row = 3, column = 3)
    lbtn = Button(root, text = "LOG OUT", command = lambda : logout_button(root))
    lbtn.grid(row = 5, column = 3, sticky = N, padx = 4, pady = 3)
    shbtn = Button(root, text = "SHARE", command = lambda : share_button(root))
    shbtn.grid(row = 4, column = 3)


def login():  #ODAVDJE DO DOLJE SVE C/P BRIŠI U KODU ONO SVE OD KLASE DO DOLJE (OVO JE SADA TO) I GORE C/P LOGOUT()

    master = Tk()
    master.title("Login")

    label_1 = Label(master, text="Username")
    label_2 = Label(master, text="Password")

    entry_1 = Entry(master)
    entry_2 = Entry(master, show="*")

    label_1.grid(row=0, sticky=E)
    label_2.grid(row=1, sticky=E)
    entry_1.grid(row=0, column=1)
    entry_2.grid(row=1, column=1)

    logbtn = Button(master, text="Login", command = lambda : login_btn_clickked(master, entry_1, entry_2))
    logbtn.grid(columnspan=2)
    regbtn = Button(master, text="Register", command = lambda: register_btn_clickked(master, entry_1, entry_2))
    regbtn.grid(columnspan=2)

    master.mainloop()

def login_btn_clickked(master, entry_1, entry_2):

    username = entry_1.get()
    password = entry_2.get()

    data= 'log' + ' ' + username + ';' + password
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.sendall(data.encode('utf-8'))
    #socket1.close()
    feedback = socket1.recv(1024).decode('utf-8')
    #print(feedback.decode('utf-8'))
    if feedback == 'true': #OVDJE POSTAVLJAŠ UVJET I AKO JE TOCAN OTVARA SE GLAVNI PROZOR
        #tm.showinfo("Login info", "Welcome %s" %username)
        global user
        user = username
        master.destroy()
        init()
    else:
        tm.showerror("Login error", "Incorrect username or password") #OVO JE AKO FULAŠ
    socket1.close()
    return

def register_btn_clickked(master, entry_1, entry_2):

    username = entry_1.get()
    password = entry_2.get()

    #registration server connection
    data= 'reg' + ' ' + username + ';' + password
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.sendall(data.encode('utf-8'))
    #socket1.close()
    feedback = socket1.recv(1024).decode('utf-8')
    if feedback == 'false': #OVDJE AKO SE PODUDARA SA VEC NEKIM
        tm.showerror("Register error","Username is already in use!")
    else:                                             #OVDJE SPERAMJ NOVOG KORISNIKA
        tm.showinfo("Register info", "Registration successful!")
    socket1.close()
    return


login()
