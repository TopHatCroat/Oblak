import socket
#import sys
import os
import ntpath
#from _thread import start_new_thread
HOST = ''    # server name goes in here
PORT = 4444

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen(10)
logged_user = ''

# def clientthread(conn):
logged_user = ''
while True:
    conn, addr = socket.accept()
    print ('New client connected ..')
    #start_new_thread(clientthread, (conn,))
    reqCommand = conn.recv(1024).decode('utf-8')
    print ('Client> %s.' %reqCommand)

    if (reqCommand == 'out'):
        print('User %s logged out.' %logged_user)
        logged_user = ''
        #break

    elif (reqCommand == 'ref'):
        #curpath = os.path.abspath(os.curdir)
        curpath = os.curdir
        path = os.path.join(curpath, logged_user)
        #files = [f for f in os.listdir('.') if os.path.isfile(os.path.join(curpath, f))]
        #files = filter(os.path.isfile, os.listdir( os.curdir ) )
        #files = [f for f in os.listdir(path) if os.path.isfile(f)]
        files = os.listdir(path)
        for f in files:
            conn.sendall(f.encode('utf-8'))


    else:
        string = reqCommand.split(' ', 1)
        reqFile = string[1]

        if (string[0] == 'put'):
            try:
                curpath = os.path.abspath(os.curdir)
                reqFile = path_leaf(string[1].strip())
                reqFile = os.path.join(curpath, logged_user, reqFile)
                #os.chdir(logged_user)
                #print(reqFile)
                with open(reqFile, 'w') as file_to_write:
                    while True:
                        data = conn.recv(1024).decode('utf-8')
                        if not data:
                            feedback = 'No file found!'
                            break
                        file_to_write.write(data)
                        file_to_write.close()
                        feedback = 'Upload successful'
                        break
            except OSError:
                feedback = 'Upload could not complete.'
            conn.sendall(feedback.encode('utf-8'))
            #print ('Receive Successful')

        elif (string[0] == 'get'):
            try:
                if(string[1][:1] == '!'):
                    reqFile = string[1][1:]
                else:
                    #os.chdir(logged_user)
                    curpath = os.path.abspath(os.curdir)
                    reqFile = path_leaf(string[1].strip())
                    reqFile = os.path.join(curpath, logged_user, reqFile)
                with open(reqFile, 'r') as file_to_send:
                    for data in file_to_send:
                        conn.sendall(data.encode('utf-8'))
                #feedback = 'Download successful'
            except OSError:
                feedback = 'Download could not complete.'
            #conn.sendall(feedback.encode('utf-8'))
            #print ('Send Successful')

        elif (string[0] == 'rem'):
            try:
                reqFile = path_leaf(string[1].strip())
                reqFile = os.path.join(logged_user, reqFile)
                os.remove(reqFile)
                feedback = 'Delete successful!'
            except OSError:
                feedback = 'File not found.'
            conn.sendall(feedback.encode('utf-8'))
            #print ('Remove Successful')

        elif (string[0] == 'shr'):
            try:
                curpath = os.path.abspath(os.curdir)
                reqFile = path_leaf(string[1].strip())
                reqFile = os.path.join(curpath, logged_user, reqFile)
                feedback = '!'+reqFile
            except OSError:
                feedback = 'Error occured.'
            conn.sendall(feedback.encode('utf-8'))

        elif (string[0] == 'reg'):
            database = open('database.txt', 'a')
            data = string[1].rstrip()
            data = data.split(';')
            directory = data[0]
            if not os.path.exists(directory):
                os.makedirs(directory)
                curpath = os.path.abspath(os.curdir)
                path = os.path.join(curpath, data[0])
                os.chmod(path, 0o777)
                data = data[0] + ';' + data[1] + '\n'
                database.write(data)
                feedback = 'true'
            else: feedback = 'false'
            database.close()
            conn.sendall(feedback.encode('utf-8'))

        elif (string[0] == 'log'):
            database = open('database.txt', 'r')
            data = string[1].rstrip()
            data = data.split(';')
            feedback = ''
            for row in database:
                row = row.rstrip()
                row = row.split(';')
                # print(data[0], ' : ', row[0])
                # print(data[1], ' : ', row[1])
                #print('...........')
                if(data[0] == row[0] and data[1] == row[1]):
                    logged_user = data[0]
                    feedback = 'true'
                    #print('Connected with '  + addr[0] + ':' + str(addr[1]))
                    print('{0} logged in. [{1}:{2}]'.format(data[0], addr[0], addr[1]))
                    break
                else: feedback = 'false'
            database.close()
            conn.sendall(feedback.encode('utf-8'))

    conn.close()

# while (1):
#     # socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # socket.bind((HOST, PORT))
#     # socket.listen(1)
#     conn, addr = socket.accept()
#     print ('New client connected ..')
#     start_new_thread(clientthread, (conn,))


socket.close()
