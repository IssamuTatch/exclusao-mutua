import socket
import datetime
import threading


def processo():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print('Connected to Server')

    for _ in range(10):
        now = str(datetime.datetime.now())

        s.send('REQUEST'.encode('ascii'))

        grant_signal = s.recv(1024).decode('ascii')

        if grant_signal == 'GRANT':
            with open('resultado.txt', 'a') as file:
                file.write(now + '|' + str(s.getsockname()) + '\n')

    s.send('RELEASE'.encode('ascii'))
    s.close()


def main():
    for _ in range(5):
        threading.Thread(target=processo).start()


if __name__ == '__main__':
    main()
