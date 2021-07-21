# cython: language_level=3
from const import const
import errors as err
import hashlib
import random
import json
import zlib


const.SEED: str = hashlib.sha1('202107202035'.encode('utf-8')).hexdigest() # Please change the string here...


def encode(cont: str, passwd: str = None, usejson: bool = True):
    if passwd is None:
        passwd = const.SEED
    if usejson:
        cont = '$$' + json.dumps(cont)
    else:
        cont = '$$' + cont
    ran = random.Random()
    ran.seed(passwd, version=2)
    lenth: int = len(cont)
    cont_i: int = int.from_bytes(cont.encode('utf-8'), 'big')
    rand_s: str = ''
    for i in range(lenth):
        rand_s += chr(ran.randint(33, 122))
    rand_i: int = int.from_bytes(rand_s.encode('utf-8'), 'big')
    result: bytes = int.to_bytes(rand_i ^ cont_i, lenth, 'big')
    result = zlib.compress(result)
    return result


def decode(cont: bytes, passwd: str = None, usejson: bool = True):
    if passwd is None:
        passwd = const.SEED
    ran = random.Random()
    ran.seed(passwd, version=2)
    cont_d: bytes = zlib.decompress(cont)
    lenth: int = len(cont_d)
    cont_i: int = int.from_bytes(cont_d, 'big')
    rand_s: str = ''
    for i in range(lenth):
        rand_s += chr(ran.randint(33, 122))
    rand_i: int = int.from_bytes(rand_s.encode('utf-8'), 'big')
    result_s: str = int.to_bytes(rand_i ^ cont_i, lenth, 'big').decode('utf-8')
    if result_s[0:2] != '$$':
        raise err.secretWrongError
    if usejson:
        result: str = json.loads(result_s[2:])
    else:
        result: str = result_s[2:]
    return result
