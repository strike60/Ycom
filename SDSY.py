import socket
import sys
import termios
import tty


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def getpass(maskchar="*"):
    password = ""
    while True:
        ch = getch()
        if ch == "\r" or ch == "\n":
            return password
        elif ch == "\b" or ord(ch) == 127:
            if len(password) > 0:
                sys.stdout.write("\b \b")
                sys.stdout.flush()
                password = password[:-1]
        else:
            if maskchar:
                sys.stdout.write(maskchar)
                sys.stdout.flush()
            password += ch


class SDSYclient(object):
    """docstring for SDSYclient"""

    def __init__(self):
        super(SDSYclient, self).__init__()
        self.__registerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__loginSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__name = None
        self.__passwd = None
        self.__email = None
        self.__gender = None

    def Register(self):
        self.__registerSock.connect(('127.0.0.1', 31415))
        print('-----------------------------------------------------------------')
        print('The SDSY is the abbreviation of \'Strike,Do not Say sorrY\'.')
        print('The software is designed to encourage me to do what I want to do!')
        print('                                                         --Strike')
        print('Warning: The software now is the beta version and DO NOT USE THE ')
        print('openssl.Do not use the real information!')
        print('-----------------------------------------------------------------')
        while True:
            print('What\'s your name?')
            self.__name = sys.stdin.readline()
            while True:
                print('Password:')
                self.__passwd = getpass()
                print('\nPassword again:')
                passwd2 = getpass()
                if self.__passwd == passwd2:
                    break
                else:
                    print('Retry!')
                    pass
            print('\nEmail:')
            self.__email = sys.stdin.readline()
            print('Male or female?')
            self.__gender = sys.stdin.readline()
            self.__registerSock.send(('%s;%s;%s;%s' % (
                self.__name, self.__passwd, self.__email, self.__gender)).encode('utf-8'))
            ret = self.__registerSock.recv(1024).decode('utf-8')
            print(ret)
            if ret == 'The name has been used.Please change the name.':
                continue
            else:
                break
        self.__registerSock.close()


    def __login(self):
        self.__loginSock.connect(('127.0.0.1', 1227))
        print(self.__loginSock.recv(1024).decode('utf-8'))
        name = sys.stdin.readline()
        self.__loginSock.send(name.encode('utf-8'))
        passwd = getpass()
        self.__loginSock.send(passwd.encode('utf-8'))
        ret = self.__loginSock.recv(1024).decode('utf-8')
        if ret == 'Welcome!\nWhat do you want to do?\n(Link, Who, Logout)':
            message = sys.stdin.readline()
                


        

    def run(self):
        while True:
            registeration = input('Do you have the account?(yes/no):')
            if registeration == 'yes':
                break
            elif registeration == 'no':
                self.Register()
                break
            else:
                pass
        

if __name__ == '__main__':
    client = SDSYclient()
    client.run()
