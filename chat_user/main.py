import keyboard as ky
import errors as err
import socket
import time
import Obj
import sys
import os


def SetKey():
    ky.add_hotkey('alt', keypressed)

def RemoveKey():
    try:
        ky.remove_hotkey('alt')
    except:
        pass

def keypressed():
    RemoveKey()
    o.Textbox(SetKey)

try:
    print('\033c', end='')
    addr_name = input('Input server: ')
    print('Finding...')
    addr_ip = socket.gethostbyname(addr_name)
    print('Find:', addr_ip)
    addr_port = int(input('Input server port: '))
    addr = (addr_ip, addr_port)
    while True:
        try:
            print('\033c', end='')
            print('Login...\n')
            room = input('Input room name: ')
            if room.lower() == '@exit':
                sys.exit()
            passwd = input('Input room secret key: ')
            o = Obj.active(addr, room, passwd)
            print('\033c', end='')
            print('You are in {} ...'.format(room))
            name = input('Set your name: ')
            if len(name) == 0 or len(name) > 10:
                raise ValueError
            o.Setname(name)
            print()
            ky.add_hotkey('alt', keypressed)
            while True:
                try:
                    time.sleep(1)
                    if o.GetStatue() == 'logout':
                        RemoveKey()
                        del o
                        print('Logout...')
                        input('\nPress ENTER to continue...\033[0m')
                        break
                    if o.GetStatue() == 'exit':
                        sys.exit()
                except KeyboardInterrupt:
                    pass
                except err.timeouterror:
                    print('connection time out...')
                    time.sleep(2)
                    raise
                except SystemExit:
                    print('EXIT')
                    input('\nPress ENTER to continue...\033[0m')
                    raise
                except:
                    print('Error:', sys.exc_info()[0])
                    raise
        except err.loginerror:
            try:
                del o
            except:
                pass
            print('Login error...')
            input('\nPress ENTER to continue...')
except ValueError:
    print('Please input rigth value...')
    input('\nPress ENTER to continue...\033[0m')
except socket.gaierror:
    print('Wrong server...')
    input('\nPress ENTER to continue...\033[0m')
