import socket


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
        self.__loginListenSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #

    def __openRegistration(self):
        self.__registrationListenSock.bind(('127.0.0.1', 31414))
        self.__registrationListenSock.listen(5)
        print('Open registration channel.')

    def __recordRegistInfo(self):
        Registsock, _ = self.__registrationListenSock.accept()
        try:
            message = Registsock.recv(1024).decode('utf-8')
            name, passwd, email, gender = message.split(';')
            if not self.__findUser(name):
                self.__registList.append(User(name, passwd, email, gender))
                Registsock.send('Regist successfully.'.encode('utf-8'))
            else:
                Registsock.send('The name has been used.Please change the name.'.encode('utf-8'))
        except:
            Registsock.send('Can not regist successfully.'.encode('utf-8'))
        finally:
            Registsock.close()

    def Register(self):
        self.__openRegistration()
        while True:
            self.__recordRegistInfo()

    def __findUser(self, name):
        for user in self.__registList:
            if name == user.get_name():
                return True
                break
        return False

    def __authenticate(self):
        pass





if __name__ == '__main__':
    a = Yserver()
    a.Register()
