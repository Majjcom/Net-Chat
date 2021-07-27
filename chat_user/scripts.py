import errors as err
import hashlib
import socket
import secret
import json
import time
import sys


# recv
def recv(s, buff: int, t0: float, timeout: int = 5):
    while True:
        tmp = s.recv(buff)
        if len(tmp) != 0:
            break
        if time.time() > t0 + timeout:
            raise err.timeouterror
    return tmp


# tryclose
def tryclose(s):
    try:
        s.close()
    except:
        pass
    try:
        del s
    except:
        pass


# get
def get(addr: tuple, room: str, passwd: str, t, name: str):
    """
    tuple->addr
    str->room
    str->passwd
    float->time
    str->name
    
    return<-float/int
    0.0: 最后时间戳
    -1: 无新消息
    -2: 错误
    """
    try:
        post = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        post['head'] = 'get'
        post['room'] = room
        post['passwd'] = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        post['time'] = t
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        s.send(post_jbe)
        get = recv(s, 1024, time.time())
        get = secret.decode(get, usejson=False)
        get = json.loads(get)
        # {'head':'no'/'pass'/'unpass','conts':int}
        if get['head'] == 'pass':
            if get['conts'] == 0:
                return -1
            else:
                for i in range(get['conts']):
                    s.send('1'.encode('utf-8'))
                    get_c = recv(s, 1024, time.time())
                    get_c = secret.decode(get_c, passwd=post['passwd'], usejson=False)
                    get_c = json.loads(get_c)
                    # ['name','cont',float]
                    if get_c[0] == name:
                        print('\033[36m', end='')
                    print('{}: {}\033[0m'.format(get_c[0], get_c[1]))
                return get_c[2]
        elif get['head'] == 'no':
            print('No such room...')
            return -2
        elif get['head'] == 'unpass':
            print('Wrong secret key...')
            return -2
        tryclose(s)
    except err.timeouterror:
        tryclose(s)
        raise
    except:
        print('\033[31mGet Error:', sys.exc_info()[0], '\033[0m')
        tryclose(s)
        # raise#
        return -2


# checkpass
def check(addr: tuple, room: str, passwd: str) -> int:
    """
    tuple->addr
    str->room
    str->passwd
    
    return<-int
    0: 正常
    -1: 无法连接
    -2: 房间不存在
    -3: 密钥错误
    -7: 未知错误
    """
    try:
        post = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        post['head'] = 'check'
        post['room'] = room
        post['passwd'] = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        s.send(post_jbe)
        get = recv(s, 128, time.time())
        get = secret.decode(get, usejson=True)
        if get == 'pass':
            return 0
        elif get == 'no':
            return -2
        elif get == 'unpass':
            return -3
        tryclose(s)
    except ConnectionRefusedError:
        tryclose(s)
        return -1
    except err.timeouterror:
        tryclose(s)
        raise
    except:
        print('\033[31mCheck Error:', sys.exc_info()[0], '\033[31m')
        tryclose(s)
        # raise#
        return -7


# send
def send(addr: tuple, room: str, passwd: str, name: str, cont: str) -> int:
    """
    tuple->addr
    str->room
    str->passwd
    str->name
    str->cont
    
    return<-int
    0: 正常
    -1: 无法连接
    -2: 内容过长
    -3: 认证错误
    -7: 未知错误
    """
    try:
        if len(cont.encode('utf-8')) > 512 or len(name) > 10:
            raise err.toolongerror
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        post = {}
        post['head'] = 'send'
        post['room'] = room
        post['passwd'] = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        post['name'] = name
        post['cont'] = cont
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        if len(post_jbe) > 1024:
            raise err.toolongerror
        s.send(post_jbe)
        get = recv(s, 512, time.time())
        get = json.loads(get.decode('utf-8'))
        if get['head'] == 'pass':
            tryclose(s)
            return 0
        elif get['head'] == 'no' or get['head'] == 'unpass':
            tryclose(s)
            return -3
        else:
            tryclose(s)
            return -7
    except ConnectionRefusedError:
        tryclose(s)
        return -1
    except err.toolongerror:
        tryclose(s)
        return -2
    except err.timeouterror:
        tryclose(s)
        raise
    except:
        print('\033[31mSend Error:', sys.exc_info()[0], '\033[31m')
        tryclose(s)
        return -7


# creat
def creat(addr: tuple, room: str, passwd: str, n_room: str, n_passwd: str) -> int:
    """
    tuple->addr
    str->name
    str->passwd
    str->n_room
    str->n_passwd
    
    return<-int
    0: 正常
    -1: 连接错误
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        post = {}
        post['head'] = 'creat'
        post['room'] = room
        post['passwd'] = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        post['n_room'] = n_room
        post['n_passwd'] = hashlib.sha256(n_passwd.encode('utf-8')).hexdigest()
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        s.send(post_jbe)
        get = recv(s, 256, time.time())
        get = json.loads(get.decode('utf-8'))
        if get['head'] == 'no':
            tryclose(s)
            return -2
        elif get['head'] == 'unpass':
            tryclose(s)
            return -3
        elif get['head'] == 'pass':
            tryclose(s)
            return 0
        elif get['head'] == 'fail':
            tryclose(s)
            return -4
        else:
            tryclose(s)
            return -7
    except ConnectionRefusedError:
        tryclose(s)
        return -1
    except:
        print('\033[31mCreat error:', sys.exc_info()[0], '\033[0m')
        tryclose(s)
        return -7


# passwd
def passwd(addr: tuple, room: str, passwd: str, n_room: str, n_passwd: str) -> int:
    """
    tuple->addr
    str->room
    str->passwd
    str->n_passwd

    return<-int
    0: 正常
    -1: 连接错误
    -2: 房间不存在
    -3: 秘钥错误
    -4: 设定失败
    -7: 为止错误
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        post = {}
        post['head'] = 'passwd'
        post['room'] = room
        post['passwd'] = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        post['n_room'] = n_room
        post['n_passwd'] = hashlib.sha256(n_passwd.encode('utf-8')).hexdigest()
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        s.send(post_jbe)
        get = recv(s, 128, time.time())
        get = secret.decode(get, usejson=False)
        get = json.loads(get)
        if get['head'] == 'pass':
            print('hash:', get['hash'])
            tryclose(s)
            return 0
        elif get['head'] == 'no':
            tryclose(s)
            return -2
        elif get['head'] == 'unpass':
            tryclose(s)
            return -3
        elif get['head'] == 'fail':
            tryclose(s)
            return -4
        else:
            tryclose(s)
            return -7
    except ConnectionRefusedError:
        tryclose(s)
        return -1
    except:
        print('\033[31mPasswd error:', sys.exc_info()[0], '\033[0m')
        tryclose(s)
        return -7


# getall
def getall(addr: tuple, room: str, passwd: str) -> int:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        post = {}
        post['head'] = 'getall'
        post['room'] = room
        post['passwd'] = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        s.send(post_jbe)
        get = recv(s, 1024, time.time())
        get = secret.decode(get, usejson=False)
        get = json.loads(get)
        if get['head'] == 'pass':
            if get['conts'] == 0:
                return -1
            else:
                for i in range(get['conts']):
                    s.send('1'.encode('utf-8'))
                    get_c = recv(s, 1024, time.time())
                    get_c = secret.decode(get_c, passwd=post['passwd'], usejson=False)
                    get_c = json.loads(get_c)
                    print('\033[0m', end='')
                    print('{}: {}\033[0m'.format(get_c[0], get_c[1]))
                return 0
        elif get['head'] == 'no':
            print('No such room...')
            return -2
        elif get['head'] == 'unpass':
            print('Wrong secret key...')
            return -2
    except ConnectionRefusedError:
        tryclose(s)
        return -1
    except err.timeouterror:
        tryclose(s)
        raise
    except:
        print('\033[31mGetall error:', sys.exc_info()[0], '\033[0m')
        tryclose(s)
        return -7


#ping
def ping(addr: tuple) -> str:
    """
    returns:
        $$x{code}: Error
        $$o{content}: Pass
    codes:
        -1: 连接失败
        -2: 连接超时
        -3: 秘钥错误
        -7: 未知错误
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        post = {}
        post['head'] = 'ping'
        post_j = json.dumps(post)
        post_jbe = secret.encode(post_j, usejson=False)
        s.send(post_jbe)
        get = recv(s, 1024, time.time(), 2)
        get = secret.decode(get, usejson=False)
        get = json.loads(get)
        return '$$o' + get['notice']
    except ConnectionRefusedError:
        tryclose(s)
        return '$$x-1'
    except err.timeouterror:
        tryclose(s)
        return '$$x-2'
    except err.secretWrongError:
        tryclose(s)
        return '$$x-3'
    except:
        tryclose(s)
        print('\033[31mPing error:', sys.exc_info()[0], '\033[0m')
        return '$$x-7'
