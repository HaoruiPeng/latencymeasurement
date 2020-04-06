import socket
import time
import threading

def Send_Handler(s, addr):
    seq_num = 0
    while True:
        stamp = time.time()
        seq_num += 1
        message = "{},{}".format(seq_num, stamp)
        print("send,"+message)
        s.sendto(message.encode('utf-8'), addr)
        pause = stamp+0.005-time.time()
        if pause > 0:
            time.sleep(pause)

def Recv_Handler(s):
    while True:
        data, addr = s.recvfrom(4096)
        data = data.decode('utf-8')
        stamp = str(time.time())
        # print(data)
        try:
            seq, _ = str(data).split(",")
            print("rec,"+seq+","+stamp)
        except:
            pass

def Main():
    # host = '129.192.69.27'
    host = "129.192.71.139"
    # host = "130.235.202.196"
    # host = "localhost"
    # host = "130.235.202.201"
    # port = 12345
    port = 31093
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("connect to socket")
    send = threading.Thread(target=Send_Handler, args=(s, (host, port),))
    recv = threading.Thread(target=Recv_Handler, args=(s, ))
    send.start()
    recv.start()
    send.join()
    recv.join()
    s.close()

if __name__ == '__main__':
    Main()
