import socket
import threading
import time

waiting_list = []
lock = threading.Lock()

# def interface():
#     while True:
#         with lock:
#             if not waiting_list:
#                 print("Waiting List: Empty")
#             else:
#                 print("Waiting List:")
#                 print(*waiting_list, sep='\n')
#         time.sleep(1)


def coordenador(c, addr):
    while True:
        decoded_data = c.recv(1024).decode('ascii')

        with lock:
            if decoded_data == 'REQUEST':
                waiting_list.append((c, addr))
                print(waiting_list)

                if waiting_list[0] == (c, addr):
                    next_c, next_addr = waiting_list[0]
                    next_c.send('GRANT'.encode('ascii'))

            if decoded_data == 'RELEASE':
                waiting_list.pop(0)
        break


def main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))
    s.listen()

    print('Server is listening...')

    while True:
        c, addr = s.accept()

        threading.Thread(target=coordenador, args=(c, addr)).start()


if __name__ == '__main__':
    threading.Thread(target=main).start()
