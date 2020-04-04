import socket
import time
import threading

def Send_Handler(s):
    seq_num = 0
    while True:
        stamp = time.time()
        seq_num += 1
        message = "{},{}".format(seq_num, stamp)
        # message sent to server
        s.send(message.encode('utf-8'))
        time.sleep(stamp+0.005-time.time())

def Recv_Handler(s):
    while True:
        data = s.recv(1024)
        print(str(data.decode('utf-8')))

def Main():
    host = '127.0.0.1'
    port = 12345
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    send = threading.Thread(target=Send_Handler, args=(s,))
    recv = threading.Thread(target=Recv_Handler, args=(s,))
    send.start()
    recv.start()
    send.join()
    recv.join()
    s.close()

if __name__ == '__main__':
    Main()
