import errors as err
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
    while True:
        try:
            room = input('Input room name: ')
            passwd = input('Input room secret key: ')
            o = Obj.active(addr, room, passwd)
            os.system('cls')
            print('You are in {} ...'.format(room))
            name = input('Set your name: ')
            if len(name) == 0 or len(name) > 10:
                raise ValueError
            o.Setname(name)
            print()
            o.Get()
            while True:
                try:
                    o.Get()
                    time.sleep(1)
                except KeyboardInterrupt:
                    try:
                        cont = input('\033[36m' + name + ': ')
                        if o.room == 'Sys':
                            cont = '@' + cont
                        if len(cont) == 0:
                            raise err.noneerror
                        if cont[0] != '@':
                            o.Send(cont)
                        else:
                            print('\033[33m', end='')
                            cont = cont.lower()
                            if cont == '@creat':
                                o.Creat()
                            elif cont == '@exit':
                                tmp = input('Really?(y)')
                                if tmp == 'y' or tmp == 'Y':
                                    raise err.exit
                            elif cont == '@logout':
                                tmp = input('Really?(y)')
                                if tmp == 'y' or tmp == 'Y':
                                    raise err.logout
                            elif cont == '@addr' or cont == '@address':
                                print('Server address is:', addr)
                            elif cont == '@clear':
                                os.system('cls')
                            elif cont == '@passwd':
                                o.Passwd()
                            else:
                                print('\033[31mSys: No such command...\033[0m')
                        print('\033[0m')
                    except KeyboardInterrupt:
                        pass
                    except err.adminloginerror:
                        print('\033[31mSys: You don\'t have admin access...\033[0m')
                        print()
                    except err.noneerror:
                        print('\033[0mPlease input something...\n')
                    except err.timeouterror:
                        raise
                    except err.exit:
                        raise
                    except err.logout:
                        raise
                    except:
                        print('\033[0mError:', sys.exc_info()[0])
                        #raise#
                except err.timeouterror:
                    print('connection time out...')
                    time.sleep(2)
                except err.logout:
                    raise
                except:
                    print('Error:', sys.exc_info()[0])
                    raise
        except err.logout:
            del o
            print('Logout...')
            input('\nPress ENTER to continue...\033[0m')
            os.system('cls')
        except err.loginerror:
            print('Login error...')
            input('\nPress ENTER to continue...')
            os.system('cls')
except ValueError:
    print('Please input rigth value...')
    input('\nPress ENTER to continue...')
except socket.gaierror:
    print('Wrong server...')
    input('\nPress ENTER to continue...')
except err.exit:
    print('EXIT')
    input('\nPress ENTER to continue...')
