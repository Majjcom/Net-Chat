import threading as thr
import scripts as src
import errors as err
import tkinter


class textinputbox(thr.Thread):
    def __init__(self, o, end):
        thr.Thread.__init__(self)
        self._o = o
        self._end = end

    def run(self):
        box = tkinter.Tk()
        box.title('Sender')
        box.geometry('300x50')
        v = tkinter.Variable()
        etr = tkinter.Entry(box, textvariable=v, width=25)
        etr.pack(side='left')

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

        btn = tkinter.Button(box, text='SEND', width=10, height=1, command=getcont)
        btn.pack(side='right')
        box.mainloop()
        self._end()


class MessageGetter(thr.Thread):
    def __init__(self, o):
        thr.Thread.__init__(self)
        self._o = o

    def run(self):
        from time import sleep
        while True:
            self._o.Get()
            if self._o.GetStatue() == 'logout' or self._o.GetStatue() == 'exit':
                break
            sleep(1)


class active:
    def __init__(self, addr: tuple, room: str, passwd: str):
        self._addr = addr
        self._room = room
        self._passwd = passwd
        tmp = src.check(addr, room, passwd)
        self._latest = 0.0
        self._statue = 'normal'
        self._name = ''
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
        n_passwd = input('Set secret key: ')
        if len(n_room) == 0 or len(n_room) > 8 or len(n_passwd) == 0:
            print('Please input right value...')
        else:
            tmp = src.creat(self._addr, self._room, self._passwd, n_room, n_passwd)
            if tmp != 0:
                print('Creat error...', tmp)
            else:
                print('Room \"{}\" created...'.format(n_room))
        input('\nPress ENTER to continue...')
        return

    def _Passwd(self):
        if self._room != 'Sys':
            print('\033[31mSys: You don\'t have access to do this...')
            return
        room = input('Input room name: ')
        passwd = input('Input secret key: ')
        n_passwd = input('Set new secret key: ')
        if len(room) == 0 or len(room) > 8 or len(passwd) == 0 or len(n_passwd) == 0:
            print('Please input right value...')
        else:
            tmp = src.passwd(self._addr, room, passwd, n_passwd)
            if tmp != 0:
                print('Set key error...', tmp)
            else:
                print('Room \"{}\"\'s Key reseted...'.format(room))
        input('\nPress ENTER to continue...')
        return

    def _Flush(self):
        self._latest = -2.0

    def _Getall(self):
        if self._room != 'Sys':
            print('\033[31mSys: You don\'t have access to do this...')
            return
        room = input('The room you want to check: ')
        passwd = input('Input secret key: ')
        tmp = src.getall(self._addr, room, passwd)
        if tmp != 0:
            print('Getall error:', tmp)

    def Textbox(self, end):
        textbox = textinputbox(self, end)
        textbox.start()
        pass

    def Command(self, *argv):
        print('\033[33m', end='')
        if argv[0] == '@creat':
            self._Creat()
        elif argv[0] == '@exit':
            tmp = input('Really?(y)')
            if tmp.lower() == 'y':
                self._statue = 'exit'
        elif argv[0] == '@logout':
            tmp = input('Really?(y)')
            if tmp.lower() == 'y':
                self._statue = 'logout'
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
        else:
            print('\033[31mSys: No such command...\033[0m')
        print('\033[0m', end='')
