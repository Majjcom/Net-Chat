import socket
import json
import time
import sys
import os


class timeouterror(Exception):
    pass


def recv(s, buff, t0):
    while True:
        tmp = s.recv(buff)
        if len(tmp) != 0:
            break
        if time.time() > t0 + 5:
            raise timeouterror
    return tmp


def checkpass(path, room, passwd):
    if os.path.exists(path + room + '.dat'):
        f = open(path + room + '.safe', 'r')
        if passwd == f.read():
            f.close()
            return 'pass'
        else:
            f.close()
            return 'unpass'
    else:
        return 'no'


try:
    addr = ('0.0.0.0', 5555)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(10)
    path_f = str(__file__)
    name = os.path.basename(path_f)
    path = path_f[:path_f.find(name)] + 'data/'
    while True:
        try:
            print('Listen to: {}'.format(addr))
            l, l_addr = s.accept()
            print('\033[33mLinker: {}\033[0m'.format(l_addr))
            get = recv(l, 1024, time.time())
            get = json.loads(get.decode('utf-8'))
            print('\033[36mget: {}\033[0m'.format(get))
            if get['head'] == 'check':
                room = get['room']
                passwd = get['passwd']
                l.send(checkpass(path, room, passwd).encode('utf-8'))
                print('\033[32mcheck finish\033[0m')
            elif get['head'] == 'get':
                room = get['room']
                passwd = get['passwd']
                t = get['time']
                post = {}
                tmp = checkpass(path, room, passwd)
                post['head'] = tmp
                if tmp == 'pass':
                    cont = []
                    f = open(path + room + '.dat', 'r')
                    cont_j = json.load(f)
                    f.close()
                    for key in cont_j:
                        if float(key) > t:
                            cont += [cont_j[key] + [float(key)]]
                    print('post:', cont)
                    post['conts'] = len(cont)
                    post_jb = json.dumps(post).encode('utf-8')
                    l.send(post_jb)
                    for i in range(len(cont)):
                        get = recv(l, 64, time.time())
                        l.send(json.dumps(cont[i]).encode('utf-8'))
                else:
                    post_jb = json.dumps(post).encode('utf-8')
                    l.send(post_jb)
                print('\033[32mget finish\033[0m')
            elif get['head'] == 'send':
                room = get['room']
                passwd = get['passwd']
                post = {}
                if os.path.exists(path + room + '.dat'):
                    f = open(path + room + '.safe', 'r')
                    tmp = f.read()
                    f.close()
                    if passwd == tmp:
                        try:
                            f = open(path + room + '.dat', 'r')
                            data = json.load(f)
                            f.close()
                            data[time.time()] = [get['name'], get['cont']]
                            f = open(path + room + '.dat', 'w')
                            json.dump(data, f)
                            f.close()
                            post['head'] = 'pass'
                        except:
                            post['head'] = '{}'.format(sys.exc_info()[0])
                            try:
                                f.close()
                            except:
                                pass
                    else:
                        post['head'] = 'unpass'
                else:
                    post['head'] = 'no'
                post_jb = json.dumps(post).encode('utf-8')
                print('post: {}'.format(post_jb))
                l.send(post_jb)
                print('\033[32msend finish\033[0m')
            elif get['head'] == 'creat':
                room = get['room']
                passwd = get['passwd']
                post = {}
                tmp = checkpass(path, room, passwd)
                post['head'] = tmp
                if room == 'Sys':
                    if tmp == 'pass':
                        try:
                            f = open(path + get['n_room'] + '.dat', 'w')
                            tmp = {'1.0': ['Sys', 'Welcome, press Ctrl+C to send message...']}
                            json.dump(tmp, f)
                            f.close()
                            f = open(path + get['n_room'] + '.safe', 'w')
                            f.write(get['n_passwd'])
                            f.close()
                        except:
                            post['head'] = 'fail'
                else:
                    post['head'] == 'fail'
                post_jb = json.dumps(post).encode('utf-8')
                l.send(post_jb)
                print('\033[32mcreat finish\033[0m')
            elif get['head'] == 'passwd':
                room = get['room']
                passwd = get['passwd']
                n_passwd = get['n_passwd']
                post = {}
                tmp = checkpass(path, room, passwd)
                post['head'] = tmp
                if room == 'Sys':
                    if tmp == 'pass':
                        try:
                            f=open(path + room + '.safe', 'w')
                            f.write(n_passwd)
                            f.close()
                            post['hash'] = n_passwd
                        except:
                            post['head'] = 'fail'
                else:
                    post['head'] == 'fail'
                post_jb = json.dumps(post).encode('utf-8')
                l.send(post_jb)
            l.close()
        except KeyboardInterrupt:
            raise
        except timeouterror:
            print('connection time out...')
            try:
                l.close()
            except:
                pass
        except:
            try:
                l.close()
            except:
                pass
            print('Error:', sys.exc_info()[0])
except ConnectionRefusedError:
    print('address already in use...')
except KeyboardInterrupt:
    print('STOP')
except:
    print('\033[31mError:', sys.exc_info()[0], '\033[0m')
    try:
        s.close()
    except:
        pass
