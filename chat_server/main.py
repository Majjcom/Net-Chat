import datetime
import socket
import secret
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


def link_check(get):
    room = get['room']
    passwd = get['passwd']
    l.send(secret.encode(checkpass(path, room, passwd), usejson=True))
    print('\033[32mcheck finish\033[0m')


def link_get(get):
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
        if len(cont) > 100:
            cont = cont[len(cont) - 100:]
        print('post:', cont)
        post['conts'] = len(cont)
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        l.send(post_jbe)
        for i in range(len(cont)):
            get = recv(l, 64, time.time())
            l.send(secret.encode(json.dumps(cont[i]), passwd=passwd, usejson=False))
    else:
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        l.send(post_jbe)
    print('\033[32mget finish\033[0m')


def link_send(get):
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


def link_creat(get):
    room = get['room']
    passwd = get['passwd']
    post = {}
    tmp = checkpass(path, room, passwd)
    post['head'] = tmp
    if room == 'Sys':
        if tmp == 'pass':
            try:
                f = open(path + get['n_room'] + '.dat', 'w')
                tmp = {'1.0': ['Sys', 'Welcome, press Alt to send message...']}
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
    print('post: {}'.format(post_jb))
    l.send(post_jb)
    print('\033[32mcreat finish\033[0m')


def link_passwd(get):
    room = get['room']
    passwd = get['passwd']
    n_room = get['n_room']
    n_passwd = get['n_passwd']
    post = {}
    tmp = checkpass(path, n_room, passwd)
    post['head'] = tmp
    if room == 'Sys':
        if tmp == 'pass':
            try:
                f = open(path + n_room + '.safe', 'w+')
                f.write(n_passwd)
                f.close()
                post['hash'] = n_passwd
            except:
                post['head'] = 'fail'
    else:
        post['head'] == 'fail'
    post_j = json.dumps(post)
    post_jbe = secret.encode(post_j, usejson=False)
    print('post: {}'.format(post_j))
    l.send(post_jbe)
    print('\033[32mpasswd finish\033[0m')


def link_getall(get):
    room = get['room']
    passwd = get['passwd']
    post = {}
    tmp = checkpass(path, room, passwd)
    post['head'] = tmp
    if tmp == 'pass':
        cont = []
        f = open(path + room + '.dat', 'r')
        cont_j = json.load(f)
        f.close()
        for key in cont_j:
            cont += [cont_j[key]]
        print('post:', cont)
        post['conts'] = len(cont)
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        l.send(post_jbe)
        for i in range(len(cont)):
            get = recv(l, 64, time.time())
            l.send(secret.encode(json.dumps(cont[i]), passwd=passwd, usejson=False))
    else:
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        l.send(post_jbe)
    print('\033[32mgetall finish\033[0m')


# main
try:
    addr = ('0.0.0.0', 5555)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(10)
    path_a = os.path.realpath(str(__file__))
    path = os.path.split(path_a)[0] + '/data/'
    ##### log stdout
    log_name = 'NC_server_log_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.log'
    log_file = open(os.path.join(os.path.split(path_a)[0], log_name), 'w')
    sys.stdout = log_file
    ##### ----------
    while True:
        try:
            print('Listen to: {}'.format(addr))
            l, l_addr = s.accept()
            print('\033[33mLinker: {} atTime: {}\033[0m'.format(l_addr, datetime.datetime.now()))
            get = recv(l, 1024, time.time())
            get = secret.decode(get, usejson=False)
            get = json.loads(get)
            print('\033[36mget: {}\033[0m'.format(get))
            if get['head'] == 'check':
                link_check(get)
            elif get['head'] == 'get':
                link_get(get)
            elif get['head'] == 'send':
                link_send(get)
            elif get['head'] == 'creat':
                link_creat(get)
            elif get['head'] == 'passwd':
                link_passwd(get)
            elif get['head'] == 'getall':
                link_getall(get)
            l.close()
        except KeyboardInterrupt:
            raise
        except timeouterror:
            print('connection timeout...')
            try:
                l.close()
            except:
                pass
        except:
            try:
                try:
                    l.send('不要再连我了啊，人家不要嘛ヽ(≧□≦)ノ'.encode('utf-8'))
                except:
                    pass
                l.close()
            except:
                pass
            print('Error:', sys.exc_info()[0])
except ConnectionRefusedError:
    print('address already in use...')
    log_file.close()
except KeyboardInterrupt:
    print('STOP')
    log_file.close()
except InterruptedError:
    print('STOP')
    log_file.close()
except:
    print('\033[31mError:', sys.exc_info()[0], '\033[0m')
    try:
        s.close()
    except:
        pass
    raise
