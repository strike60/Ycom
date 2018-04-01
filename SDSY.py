import socket
import threading
import sys
import time
import getpass



# def getch():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch


# def getpass(maskchar="*"):
#     password = ""
#     while True:
#         ch = getch()
#         if ch == "\r" or ch == "\n":
#             return password
#         elif ch == "\b" or ord(ch) == 127:
#             if len(password) > 0:
#                 sys.stdout.write("\b \b")
#                 sys.stdout.flush()
#                 password = password[:-1]
#         else:
#             if maskchar:
#                 sys.stdout.write(maskchar)
#                 sys.stdout.flush()
#             password += ch


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
        self.__logSuccess = False
        self.__linkSuccess = False
        self.__logOut = False
        self.__linkerOffline = False

    def Register(self):
        self.__registerSock.connect(('23.83.246.101', 31415))
        print('--------------------------------------------------------------------')
        print('The SDSY is the abbreviation of \'Strike,Do not Say sorrY\'.')
        print('The software is designed to encourage him to do what he wants to do!')
        print('                                                            --Strike')
        print('Warning: The software now is the beta version and DO NOT USE THE ')
        print('openssl.Do not use the real information!')
        print('--------------------------------------------------------------------')
        while True:
            self.__name = input('What\'s your name?:')
            while True:
                self.__passwd = getpass.getpass('Enter the password:')
                passwd2 = getpass.getpass('Enter the password again:')
                if self.__passwd == passwd2:
                    break
                else:
                    print('Retry!')
                    pass
            self.__email = input('Email: ')
            self.__gender = input('Gender: ')
            self.__registerSock.send(('%s;%s;%s;%s' % (
                self.__name, self.__passwd, self.__email, self.__gender)).encode('utf-8'))
            ret = self.__registerSock.recv(1024).decode('utf-8')
            print(ret)
            if ret == 'The name has been used.Please change the name.':
                continue
            else:
                break
        self.__registerSock.close()


    def __sendMessage(self):
        print('(In session, you can input \'sorrY\' to exit the session.)\n')
        while True:
            if self.__linkerOffline:
                break
            if self.__logOut:
                break
            message = input()
            if message.strip() == 'sorrY':
                self.__loginSock.send((message).encode('utf-8'))
                print('Exit the session successfully.')
                break
            self.__loginSock.send((self.__name.strip('\n')+ ':' + message).encode('utf-8'))


    def __recvMessage(self):
        while True:
            if self.__logOut:
                break
            recvmessage = self.__loginSock.recv(1024).decode('utf-8')
            if recvmessage.strip() == 'Welcome!\nWhat do you want to do?\n(Link, Who, Logout)':
                self.__logSuccess = True
            if recvmessage.strip() == 'LinkOk':
                self.__linkSuccess = True
            if recvmessage.strip() == 'Opposite side is Offline, input \'sorrY\' to exit the session.':
                self.__linkerOffline = True
            print(recvmessage.strip())


    def __login(self):
        self.__loginSock.connect(('23.83.246.101', 1227))
        print(self.__loginSock.recv(1024).decode('utf-8'))
        self.__name = input()
        self.__loginSock.send(self.__name.encode('utf-8'))
        print(self.__loginSock.recv(1024).decode('utf-8'))
        self.__passwd = getpass.getpass('')
        self.__loginSock.send(self.__passwd.encode('utf-8'))
        recvthread = threading.Thread(target=self.__recvMessage, args=())
        recvthread.start()
        print('loading...')
        time.sleep(5)
        while True:
            if self.__logSuccess:
                message = input()
                self.__loginSock.send(message.encode('utf-8'))
                if message.strip()  == 'Link':
                    message = input()
                    self.__loginSock.send(message.encode('utf-8'))
                    print('linking...')
                    time.sleep(3)
                    if self.__linkSuccess:
                        self.__linkerOffline = False
                        sendthread = threading.Thread(target=self.__sendMessage, args=())
                        sendthread.start()
                        sendthread.join()
                    self.__linkSuccess = False
                    continue
                elif message.strip() == 'Who':
                    continue
                elif message.strip() == 'Logout':
                    self.__logOut = True
                    self.__logSuccess = False
                    break
            else:
                self.__logOut = True
                self.__loginSock.close()
                print('Exit!')
                break


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
        self.__login()


if __name__ == '__main__':
    client = SDSYclient()
    client.run()
