import scripts as scr
import errors as err


class active:
    addr = tuple([])
    room = ''
    passwd = ''
    name = ''
    latest = 0.0

    def __init__(self, addr, room, passwd):
        self.addr = addr
        self.room = room
        self.passwd = passwd
        tmp = scr.check(addr, room, passwd)
        if tmp != 0:
            if tmp == -1:
                print('Connect Failed...')
            elif tmp == -2:
                print('No such room...')
            elif tmp == -3:
                print('Wrong secret key...')
            else:
                print('Unknown login error...', tmp)
            raise err.loginerror
        return

    def Setname(self, name):
        self.name = name

    def Send(self, cont):
        tmp = scr.send(self.addr, self.room, self.passwd, self.name, cont)
        if tmp != 0:
            print('Send error:', tmp)
        return

    def Get(self):
        if self.latest > 0:
            n = self.name
        else:
            n = ' '
        tmp = scr.get(self.addr, self.room, self.passwd, self.latest, n)
        if tmp != -1:
            self.latest = tmp
        return

    def Creat(self):
        if self.room != 'Sys':
            raise err.adminloginerror
        n_room = input('Set room name: ')
        n_passwd = input('Set secret key: ')
        if len(n_room) == 0 or len(n_room) > 8 or len(n_passwd) == 0:
            print('Please input right value...')
        else:
            tmp = scr.creat(self.addr, self.room, self.passwd, n_room, n_passwd)
            if tmp != 0:
                print('Creat error...', tmp)
            else:
                print('Room \"{}\" created...'.format(n_room))
        input('\nPress ENTER to continue...')
        return

    def Passwd(self):
        if self.room != 'Sys':
            raise  err.adminloginerror
        room = input('Input room name: ')
        passwd = input('Input secret key: ')
        n_passwd = input('Set new secret key: ')
        if len(room) == 0 or len(room) > 8 or len(passwd) == 0 or len(n_passwd) == 0:
            print('Please input right value...')
        else:
            tmp = scr.passwd(self.addr, room, passwd, n_passwd)
            if tmp != 0:
                print('Set key error...', tmp)
            else:
                print('Room \"{}\"\'s Key reseted...'.format(room))
        input('\nPress ENTER to continue...')
        return
