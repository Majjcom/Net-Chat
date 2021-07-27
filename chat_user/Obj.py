import threading as thr
import scripts as src
import errors as err
import tkinter
import getpass


class textinputbox(thr.Thread):
    def __init__(self, o, end):
        thr.Thread.__init__(self)
        self._o = o
        self._end = end

    def run(self):
        box = tkinter.Tk()
        box.title('SendBox')
        box.geometry('300x40+200+200')
        v = tkinter.Variable()
        etr = tkinter.Entry(box, textvariable=v, width=1000)

        def getcont():
            cont = v.get()
            if self._o.GetRoom() == 'Sys':
                cont = '@' + cont
            if len(cont) != 0:
                if cont[0] != '@':
                    self._o.Send(cont)
                else:
                    cont = cont.lower()
                    self._o.Command(cont)
            box.destroy()

        btn = tkinter.Button(box, text='SEND', width=8, height=1, command=getcont)
        btn.pack(side='right')
        etr.pack(side='left')
        box.mainloop()
        self._end()


class MessageGetter(thr.Thread):
    def __init__(self, o):
        thr.Thread.__init__(self)
        self._o = o

    def run(self):
        from time import sleep
        while True:
            if self._o.GetStatue()[1] != 'pause':
                self._o.Get()
            if self._o.GetStatue()[0] == 'logout' or self._o.GetStatue()[0] == 'exit':
                break
            sleep(1)


class active:
    def __init__(self, addr: tuple, room: str, passwd: str):
        self._addr: tuple = addr
        self._room: str = room
        self._passwd: str = passwd
        tmp = src.check(addr, room, passwd)
        self._latest = 0.0
        self._statue = ['normal', 'continue']
        self._name: str = ''
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

    def Setname(self, name: str):
        self._name = name
        if self._room != 'Sys':
            getter = MessageGetter(self)
            getter.start()

    def Send(self, cont: str):
        tmp = src.send(self._addr, self._room, self._passwd, self._name, cont)
        if tmp != 0:
            print('Send error:', tmp)
        return

    def Get(self):
        tmp = src.get(self._addr, self._room, self._passwd, self._latest, self._name)
        if tmp != -1:
            self._latest = tmp
        return

    def GetStatue(self):
        return self._statue

    def GetRoom(self):
        return self._room

    def _Creat(self):
        if self._room != 'Sys':
            print('\033[31mSys: You don\'t have access to do this...')
            return
        n_room = input('Set room name: ')
        n_passwd = getpass.getpass('Set secret key: ')
        tmp = getpass.getpass('Please input again: ')
        if n_passwd != tmp:
            print('\033[31mTwo input have somthing different...')
            return
        if len(n_room) == 0 or len(n_room) > 8 or len(n_passwd) == 0:
            print('Please input right value...')
        else:
            tmp = src.creat(self._addr, self._room, self._passwd, n_room, n_passwd)
            if tmp != 0:
                print('Creat error...', tmp)
            else:
                print('Room \"{}\" created...'.format(n_room))
        input('\nFinish...')
        return

    def _Passwd(self):
        if self._room != 'Sys':
            print('\033[31mSys: You don\'t have access to do this...')
            return
        room = input('Input room name: ')
        passwd = getpass.getpass('Input secret key: ')
        n_passwd = getpass.getpass('Set new secret key: ')
        tmp = getpass.getpass('Please input again: ')
        if n_passwd != tmp:
            print('\033[31mTwo input have something different...')
            return
        if len(room) == 0 or len(room) > 8 or len(passwd) == 0 or len(n_passwd) == 0:
            print('Please input right value...')
        else:
            tmp = src.passwd(self._addr, self._room, passwd, room, n_passwd)
            if tmp != 0:
                print('Set key error...', tmp)
            else:
                print('Room \"{}\"\'s Key reseted...'.format(room))
        input('\nFinish...')
        return

    def _Flush(self):
        self._latest = -2.0

    def _Getall(self):
        if self._room != 'Sys':
            print('\033[31mSys: You don\'t have access to do this...')
            return
        room = input('The room you want to check: ')
        passwd = getpass.getpass('Input secret key: ')
        print('Start...\033[0m')
        tmp = src.getall(self._addr, room, passwd)
        print('\033[33mFinish...')
        if tmp != 0:
            print('Getall error:', tmp)

    def _Ping(self):
        tmp = src.ping(self._addr)
        if tmp[:3] == '$$x':
            if tmp[3:] == '-3':
                raise err.secretWrongError
            raise err.pingerror(tmp)
        elif tmp[:3] == '$$o':
            pass
        else:
            raise err.pingerror(tmp)
        return tmp[3:]

    def Textbox(self, end):
        textbox = textinputbox(self, end)
        textbox.start()
        pass

    def Command(self, *argv):
        self._statue[1] = 'pause'
        print('\033[33m', end='')
        if argv[0] == '@creat':
            self._Creat()
        elif argv[0] == '@exit':
            tmp = input('Really?(y)')
            if tmp.lower() == 'y':
                self._statue[0] = 'exit'
            else:
                print('okey...')
        elif argv[0] == '@logout':
            tmp = input('Really?(y)')
            if tmp.lower() == 'y':
                self._statue[0] = 'logout'
            else:
                print('okey...')
        elif argv[0] == '@addr':
            print('Server address is:', self._addr)
        elif argv[0] == '@clear':
            print('\033c')
        elif argv[0] == '@passwd':
            self._Passwd()
        elif argv[0] == '@flush':
            self._Flush()
        elif argv[0] == '@getall':
            self._Getall()
        elif argv[0] == '@ping':
            try:
                tmp = self._Ping()
                print('Ping start...\n\n', 'Notice:\n', tmp, '\n', sep='')
                print('Ping finish...')
            except:
                print('Ping ERROR...')
        elif argv[0] == '@傻逼':
            print('\033[31mSys: 你才傻逼...')
        elif argv[0] == 'oth':
            if argv[1] == 'pause':
                self._statue[1] = 'pause'
            elif argv[1] == 'continue':
                self._statue[1] = 'normal'
        else:
            print('\033[31mSys: No such command...\033[0m')
        self._statue[1] = 'continue'
        print('\033[0m', end='')


class active_ping(active):
    def __init__(self, addr: tuple):
        self._addr: tuple = addr
        tmp = self._Ping()
        print('Notice:\n', tmp, '\n', sep='')
        return
