import socket
import datetime
import threading
import time

lock = threading.Lock()


def processo():
    host = '127.0.0.1'
    port = 3000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print('Connected to Server')

    for _ in range(5):
        processo_port = s.getsockname()[1]
        s.send(('1|'+str(processo_port)+'|00').encode('ascii'))
        grant_signal = s.recv(1024).decode('ascii')

        if grant_signal.startswith('2|') and grant_signal.endswith('|00') and grant_signal[2:7].isdigit():
            with lock:
                with open('resultado.txt', 'a') as file:
                    now = str(datetime.datetime.now())
                    file.write(str(s.getsockname()) + '|' + now  +  '\n')
                time.sleep(1)
            s.send(('3|'+str(processo_port)+'|00').encode('ascii'))
            time.sleep(1)

    s.close()


def main():
    for _ in range(5):
        threading.Thread(target=processo).start()


if __name__ == '__main__':
    main()
