import socket
import threading
import time

waiting_list = []
lock = threading.Lock()

def interface():
    while True:
        with lock:
            if not waiting_list:
                print("Waiting List: Empty")
            else:
                print("Waiting List:")
                print(*waiting_list, sep='\n')
        time.sleep(1)

def coordenador(c, addr):
    try:    
        # threading.Thread(target=interface).start()

        data = c.recv(1024)

        if not data:
            with lock:
                print(f'{addr[0]}:{addr[1]} disconnected')              

        decoded_data = data.decode('ascii')

        waiting_list.append(f'{addr[0]}:{addr[1]}')

        # if decoded_data == 'REQUEST':
        #     with lock:
        #         if not waiting_list:
        #             c.send('GRANT'.encode('ascii'))
        #             waiting_list.append(f'{addr[0]}:{addr[1]}')
        #         else:
        #             c.send('WAIT'.encode('ascii'))

        # if decoded_data == 'RELEASE':
        #     with lock:
        #         if f'{addr[0]}:{addr[1]}' in waiting_list:
        #             waiting_list.remove(f'{addr[0]}:{addr[1]}')



        for i in range(len(waiting_list)):
            print(f'{i + 1} - {waiting_list[i]}')

    finally:
        c.close()

def main():
    host = '127.0.0.1'
    port = 3000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    s.listen()

    print('Server is listening...')

    while True:
        c, addr = s.accept()
        print('Connection from: ' + str(addr))

        threading.Thread(target=coordenador, args=(c, addr)).start()

if __name__ == '__main__':
    threading.Thread(target=main).start()