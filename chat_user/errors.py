class loginerror(Exception):
    pass
class toolongerror(Exception):
    pass
class noneerror(Exception):
    pass
class timeouterror(Exception):
    pass
class secretWrongError(Exception):
    pass
class pingerror(Exception):
    def __init__(self, code):
        Exception.__init__(self)
        print('PingError:', code)
        if code[3:] == '-1':
            print('ConnectionRefused...')
        elif code[3:] == '-2':
            print('Timeout...')
        elif code[3:] == '-3':
            print('SecretWrong...')
        else:
            print('Unknown...')
        print()
    pass
