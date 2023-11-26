import socket
import threading
import time
import sys

waiting_list = []
lock = threading.Lock()
identificador_count = {}

def coordenador(c, addr):
    while True:
        with lock:
            decoded_data = c.recv(1024).decode('ascii')

            if decoded_data.startswith('1|') and decoded_data.endswith('|00') and decoded_data[2:7].isdigit():
                if identificador_count.get(decoded_data[2:7]):
                    pass
                else:
                    identificador_count[decoded_data[2:7]] = 0
                #print(decoded_data)
                waiting_list.append((c, addr))

                if waiting_list[0] == (c, addr):
                    next_c, next_addr = waiting_list[0]
                    grant_mensage = '2|'+str(decoded_data[2:7])+'|00'
                    #print(grant_mensage)
                    next_c.send(grant_mensage.encode('ascii'))
                    identificador_count[decoded_data[2:7]] = identificador_count.get(decoded_data[2:7])+1
                    #print(decoded_data)

            if decoded_data.startswith('3|') and decoded_data.endswith('|00') and decoded_data[2:7].isdigit():
                #print(decoded_data)
                waiting_list.pop(0)

                if waiting_list:
                    next_c, next_addr = waiting_list[0]
                    next_c.send(('2|'+str(decoded_data[2:7])+'|00').encode('ascii'))


def main():
    host = '127.0.0.1'
    port = 3000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))
    s.listen()

    print('Server is listening...')

    while True:
        c, addr = s.accept()
        threading.Thread(target=coordenador, args=(c, addr), daemon=True).start()


if __name__ == '__main__':
    threading.Thread(target=main, daemon=True).start()
    time.sleep(1)
    print('1 - Imprimir a fila de pedidos atual')
    print('2 - Imprimir quantas vezescada processo foi atendido')
    print('3 - Encerrar a execução')
    while True:
        command = input('>> ')
        if command.lower() == '1':
            print(waiting_list)
        elif command.lower() == '2':
            print(identificador_count)
        elif command.lower() == '3':
            sys.exit("Finalizando o programa")