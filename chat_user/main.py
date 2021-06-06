import errors as Err
import socket
import time
import Obj
import sys
import os

# gethostbyname
try:
    addr_name = input('Input server: ')
    print('Finding...')
    addr_ip = socket.gethostbyname(addr_name)
    print('Find:', addr_ip)
    addr_port = int(input('Input server port: '))
    addr = (addr_ip, addr_port)
    room = input('Input room name: ')
    passwd = input('Input room secret key: ')
    name = input('Set your name: ')
    if len(name) == 0 or len(name) > 10:
        raise ValueError
    o = Obj.active(addr, room, passwd, name)
    os.system('cls')
    print('You are in {} ...'.format(room))
    o.get()
    while True:
        try:
            o.get()
            time.sleep(1)
        except KeyboardInterrupt:
            try:
                cont = input('\033[36m' + name + ': ')
                if o.room == 'Sys':
                    cont = '@' + cont
                if len(cont) == 0:
                    raise Err.noneerror
                if cont[0] != '@':
                    o.send(cont)
                else:
                    print('\033[33m', end='')
                    cont = cont.lower()
                    if cont == '@creat':
                        if o.room != 'Sys':
                            raise Err.adminloginerror
                        n_room = input('Set room name: ')
                        n_passwd = input('Set secret key: ')
                        if len(n_room) == 0 or len(n_room) > 8 or len(n_passwd) == 0:
                            print('Please input right value...')
                        else:
                            o.creat(n_room, n_passwd)
                    elif cont == '@logout' or cont == '@exit':
                        tmp = input('Really?(y)')
                        if tmp == 'y' or tmp == 'Y':
                            raise Err.exit
                    elif cont == '@addr' or cont == '@address':
                        print('Server address is:', addr)
                    else:
                        print('\033[31mSys: No such command...\033[0m')
                print('\033[0m')
            except KeyboardInterrupt:
                pass
            except Err.adminloginerror:
                print('\033[31mSys: You don\'t have admin access...\033[0m')
                print()
            except Err.noneerror:
                print('\033[0mPlease input something...\n')
            except Err.timeouterror:
                raise
            except Err.exit:
                raise
            except:
                print('\033[0mError:', sys.exc_info()[0])
                # raise#
        except Err.timeouterror:
            print('connection time out...')
            time.sleep(2)
        except:
            print('Error:', sys.exc_info()[0])
            raise
except ValueError:
    print('Please input rigth value...')
    input('\nPress ENTER to continue...')
except socket.gaierror:
    print('Wrong server...')
    input('\nPress ENTER to continue...')
except Err.loginerror:
    print('Login error...')
    input('\nPress ENTER to continue...')
except Err.exit:
    print('EXIT')
    input('\nPress ENTER to continue...')
