import socket
import threading

waiting_list = []
lock = threading.Lock()


def coordenador(c, addr):
    while True:
        with lock:
            decoded_data = c.recv(1024).decode('ascii')

            if decoded_data == 'REQUEST':
                print('REQUEST')
                waiting_list.append((c, addr))

                if waiting_list[0] == (c, addr):
                    next_c, next_addr = waiting_list[0]
                    print('GRANT')
                    next_c.send('GRANT'.encode('ascii'))

            if decoded_data == 'RELEASE':
                print('RELEASE')
                waiting_list.pop(0)

                if waiting_list:
                    next_c, next_addr = waiting_list[0]
                    next_c.send('GRANT'.encode('ascii'))


def main():
    host = '127.0.0.1'
    port = 3000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))
    s.listen()

    print('Server is listening...')

    while True:
        c, addr = s.accept()

        threading.Thread(target=coordenador, args=(c, addr)).start()


if __name__ == '__main__':
    threading.Thread(target=main).start()
