import socket
import time
import threading

def Send_Handler(s):
    seq_num = 0
    while True:
        stamp = time.time()
        seq_num += 1
        message = "{},{}".format(seq_num, stamp)
        print("send,"+message)
        s.send(message.encode('utf-8'))
        pause = stamp+0.005-time.time()
        if pause > 0:
            time.sleep(pause)

def Recv_Handler(s):
    while True:
        data = s.recv(1024).decode('utf-8')
        stamp = str(time.time())
        try:
            seq, _ = str(data).split(",")
            print("rec,"+seq+","+stamp)
        except:
            pass

def Main():
    # host = '129.192.69.27'
    host = "130.235.202.196"
    port = 12345
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    print("connect to socket")
    send = threading.Thread(target=Send_Handler, args=(s,))
    recv = threading.Thread(target=Recv_Handler, args=(s,))
    send.start()
    recv.start()
    send.join()
    recv.join()
    s.close()

if __name__ == '__main__':
    Main()
