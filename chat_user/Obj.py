import scripts as scr
import errors as err


class active:
    addr = tuple([])
    room = ''
    passwd = ''
    name = ''
    latest = 0.0

    def __init__(self, addr, room, passwd, name):
        self.addr = addr
        self.room = room
        self.passwd = passwd
        self.name = name
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

    def send(self, cont):
        tmp = scr.send(self.addr, self.room, self.passwd, self.name, cont)
        if tmp != 0:
            print('Send error:', tmp)
        return

    def get(self):
        if self.latest > 0:
            n = self.name
        else:
            n = ' '
        tmp = scr.get(self.addr, self.room, self.passwd, self.latest, n)
        if tmp != -1:
            self.latest = tmp
        return

    def creat(self, n_room, n_passwd):
        tmp = scr.creat(self.addr, self.room, self.passwd, n_room, n_passwd)
        if tmp != 0:
            print('Creat error...', tmp)
        else:
            print('Room \"{}\" created...'.format(n_room))
        return
