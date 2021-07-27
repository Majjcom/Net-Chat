import threading as thr
import errors as err
import datetime
import socket
import secret
import atexit
import json
import time
import sys
import os


class taker(thr.Thread):
    def __init__(self, l, get):
        thr.Thread.__init__(self)
        self._l = l
        self._get = get
    
    def run(self):
        try:
            if self._get['head'] == 'get':
                link_get(self._l, self._get)
            elif self._get['head'] == 'send':
                link_send(self._l, self._get)
            elif self._get['head'] == 'check':
                link_check(self._l, self._get)
            elif self._get['head'] == 'creat':
                link_creat(self._l, self._get)
            elif self._get['head'] == 'passwd':
                link_passwd(self._l, self._get)
            elif self._get['head'] == 'getall':
                link_getall(self._l, self._get)
            elif self._get['head'] == 'ping':
                link_ping(self._l, self._get)
            self._l.close()
            del self._l
        except err.timeouterror:
            print('connection timeout...')
            try:
                self._l.close()
            except:
                pass
            try:
                del self._l
            except:
                pass
        except:
            print('Error:', sys.exc_info()[0])


def end():
    print('STOP')
    try:
        log_file.close()
    except:
        pass


def recv(s, buff, t0):
    while True:
        tmp = s.recv(buff)
        if len(tmp) != 0:
            break
        if time.time() > t0 + 5:
            raise err.timeouterror
    return tmp


def checkpass(path, room, passwd):
    if os.path.exists(os.path.join(path, room + '.dat')):
        f = open(os.path.join(path, room + '.safe'), 'r')
        if passwd == f.read():
            f.close()
            return 'pass'
        else:
            f.close()
            return 'unpass'
    else:
        return 'no'


def link_check(l, get):
    room = get['room']
    passwd = get['passwd']
    l.send(secret.encode(checkpass(path_d, room, passwd), usejson=True))
    print('\033[32mcheck finish\033[0m')


def link_get(l, get):
    room = get['room']
    passwd = get['passwd']
    t = get['time']
    post = {}
    tmp = checkpass(path_d, room, passwd)
    post['head'] = tmp
    if tmp == 'pass':
        cont = []
        f = open(os.path.join(path_d, room + '.dat'), 'r')
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


def link_send(l, get):
    room = get['room']
    passwd = get['passwd']
    post = {}
    if os.path.exists(os.path.join(path_d, room + '.dat')):
        f = open(os.path.join(path_d, room + '.safe'), 'r')
        tmp = f.read()
        f.close()
        if passwd == tmp:
            try:
                f = open(os.path.join(path_d, room + '.dat'), 'r')
                data = json.load(f)
                f.close()
                data[time.time()] = [get['name'], get['cont']]
                f = open(os.path.join(path_d, room + '.dat'), 'w')
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


def link_creat(l, get):
    room = get['room']
    passwd = get['passwd']
    post = {}
    tmp = checkpass(path_d, room, passwd)
    post['head'] = tmp
    if room == 'Sys':
        if tmp == 'pass':
            try:
                f = open(os.path.join(path_d, get['n_room'] + '.dat'), 'w')
                tmp = {'1.0': ['Sys', 'Welcome, press Alt to send message...']}
                json.dump(tmp, f)
                f.close()
                f = open(os.path.join(path_d, get['n_room'] + '.safe'), 'w')
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


def link_passwd(l, get):
    room = get['room']
    passwd = get['passwd']
    n_room = get['n_room']
    n_passwd = get['n_passwd']
    post = {}
    tmp = checkpass(path_d, n_room, passwd)
    post['head'] = tmp
    if room == 'Sys':
        if tmp == 'pass':
            try:
                f = open(os.path.join(path_d, n_room + '.safe'), 'w+')
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


def link_getall(l, get):
    room = get['room']
    passwd = get['passwd']
    post = {}
    tmp = checkpass(path_d, room, passwd)
    post['head'] = tmp
    if tmp == 'pass':
        cont = []
        f = open(os.path.join(path_d, room + '.dat'), 'r')
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


def link_ping(l, get):
    post = {}
    post['head'] = 'pass'
    try:
        f = open(os.path.join(path_d, 'notice/notice'), 'rb')
        post['notice'] = f.read().decode()
        f.close()
    except:
        post['notice'] = 'None'
    if len(post['notice']) == 0 or len(post['notice']) > 512:
        post['notice'] = 'None'
    post_j = json.dumps(post)
    post_jbe = secret.encode(post_j, usejson=False)
    l.send(post_jbe)
    print('\033[32mping finish\033[0m')


# main
try:
    addr = ('0.0.0.0', 5555)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(10)
    path_a = os.path.realpath(str(__file__))
    path = os.path.split(path_a)[0]
    path_d = os.path.join(path, 'data')
    ##### log stdout

    log_name = 'NC_server_log_{}.log'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    log_file = open(os.path.join(path, log_name), 'w')
    sys.stdout = log_file
    atexit.register(end)

    ##### ----------
    while True:
        try:
            print('Listen to: {}'.format(addr))
            l, l_addr = s.accept()
            print('\033[33mLinker: {} atTime: {}\033[0m'.format(l_addr, datetime.datetime.now()))
            get = recv(l, 1024, time.time())
            get_d = secret.decode(get, usejson=False)
            get = json.loads(get_d)
            print('\033[36mget: {}\033[0m'.format(get))
            tmp = taker(l, get)
            tmp.start()
        except KeyboardInterrupt:
            raise
        except err.secretWrongError:
            print('SecretWrong...')
            try:
                print('UnknowGet:\n\033[31mStart\033[0m\n{}\n\033[31mEnd\033[0m'.format(get))
            except:
                pass
            try:
                l.send('别连了别连了，我超级难受哒，好不好嘛ヾ(。￣□￣)ﾂ゜゜゜'.encode('utf-8'))
            except:
                pass
            try:
                l.close()
            except:
                pass
            try:
                del l
            except:
                pass
        except:
            print('Error:', sys.exc_info()[0])
            try:
                l.close()
            except:
                pass
            try:
                del l
            except:
                pass
except ConnectionRefusedError:
    print('address already in use...')
    log_file.close()
except KeyboardInterrupt:
    end()
except InterruptedError:
    end()
except:
    print('\033[31mError:', sys.exc_info()[0], '\033[0m')
    try:
        s.close()
    except:
        pass
    raise
