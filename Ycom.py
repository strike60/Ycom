import socket
import threading


# Get the host's ip address
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class User(object):
    """docstring for User"""

    def __init__(self, _name, _passwd, _email, _gender):
        super(User, self).__init__()
        self.__name = _name
        self.__passwd = _passwd
        self.__email = _email
        self.__gender = _gender

    def get_name(self):
        return self.__name

    def get_passwd(self):
        return self.__passwd

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def make_record_entry(self):
        return dict({'name': self.__name,
                     'passwd': self.__passwd,
                     'email': self.__email,
                     'gender': self.__gender})


class Yserver(object):
    """docstring for Yserver"""

    def __init__(self):
        super(Yserver, self).__init__()
        self.__ip = get_host_ip()
        self.__registList = []
        self.__onlineList = []
        self.__registrationListenSock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # To receive registration info
        self.__loginListenSock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    # utils
    def __utilsFindUser(self, name):
        for user in self.__registList:
            if name == user.get_name():
                return True
        return False

    def __utilsAuthenticate(self, name, passwd):
        for user in self.__registList:
            if name == user.get_name():
                if passwd == user.get_passwd():
                    return True
                else:
                    return False
        return False

    def __utilsListOnlineUsers(self):
        userslist = ''
        for user in self.__onlineList:
            userslist = userslist + user[0].strip('\n') + ';'
        return userslist

    def __utilsLink(self, name):
        for user in self.__onlineList:
            if name == user[0]:
                return user[1]
        return None

    # Registration
    def __openRegistration(self):
        self.__registrationListenSock.bind((self.__ip, 31415))
        self.__registrationListenSock.listen(5)
        print('Open registration channel.')

    def __recordRegistInfo(self):
        Registsock, _ = self.__registrationListenSock.accept()
        try:
            while True:
                message = Registsock.recv(1024).decode('utf-8')
                name, passwd, email, gender = message.split(';')
                if not self.__utilsFindUser(name):
                    self.__registList.append(User(name, passwd, email, gender))
                    Registsock.send('Regist successfully.'.encode('utf-8'))
                    break
                else:
                    Registsock.send(
                        'The name has been used.Please change the name.'.encode('utf-8'))
        except:
            Registsock.send('Can not regist successfully.'.encode('utf-8'))
        finally:
            Registsock.close()

    def __Register(self):
        while True:
            self.__recordRegistInfo()

    # Authentication
    def __openAuthentication(self):
        self.__loginListenSock.bind((self.__ip, 1227))
        self.__loginListenSock.listen(5)
        print('Open authentication channel.')

    def __Authentication(self):
        communication_sock, addr = self.__loginListenSock.accept()
        t = threading.Thread(target=self.__iteraction, args=(communication_sock, ))
        t.start()

    def __iteraction(self, communication_sock):
        communication_sock.send('Who are you?'.encode('utf-8'))
        username = communication_sock.recv(1024).decode('utf-8')
        communication_sock.send('Password:'.encode('utf-8'))
        passwd = communication_sock.recv(1024).decode('utf-8')
        if self.__utilsAuthenticate(username, passwd):
            self.__onlineList.append((username, communication_sock))
            while True:
                communication_sock.send('Welcome!\nWhat do you want to do?\n(Link, Who, Logout)'.encode('utf-8'))
                # User's option
                option = communication_sock.recv(1024).decode('utf-8')
                if option.strip() == 'Who':
                    communication_sock.send('The online users:{}\n'.format(self.__utilsListOnlineUsers()).encode('utf-8'))
                    continue
                if option.strip() == 'Link':
                    communication_sock.send('Who?'.encode('utf-8'))
                    name = communication_sock.recv(1024).decode('utf-8')
                    destiny_sock = self.__utilsLink(name)
                    if destiny_sock:
                        communication_sock.send('LinkOk'.encode('utf-8'))
                        poxyt = threading.Thread(target=self.__Yproxy, args=(communication_sock, destiny_sock))
                        poxyt.start()
                        poxyt.join()
                        continue
                    else:
                        communication_sock.send('{} is offline'.format(name.strip('\n')).encode('utf-8'))
                        continue
                if option.strip() == 'Logout':
                    communication_sock.send('Logout successfully!'.encode('utf-8'))
                    self.__onlineList.remove((username, communication_sock))
                    communication_sock.close()
                    break
                else:
                    communication_sock.send('Wrong option!\n'.encode('utf-8'))
                    continue
        else:
            communication_sock.send('Wrong username or password!'.encode('utf-8'))
            communication_sock.close()
        



    def __Yproxy(self, hostsock, guestsock):
        while True:
            message = hostsock.recv(1024).decode('utf-8')
            if message != 'sorrY':
                try:
                    guestsock.send(message.encode('utf-8'))
                except:
                    hostsock.send('Opposite side is Offline, input \'sorrY\' to exit the session.'.encode('utf-8'))
            else:
                break


    def __Authenticate(self):
        while True:
            self.__Authentication()

    def run(self):
        self.__openRegistration()
        self.__openAuthentication()
        t1 = threading.Thread(target=self.__Register, args=())
        t2 = threading.Thread(target=self.__Authenticate, args=())
        t1.start()
        t2.start()


if __name__ == '__main__':
    a = Yserver()
    a.run()
