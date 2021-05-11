import socket
import time
import threading
import argparse
import numpy as np
import pandas as pd
import os

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--dir', action="store")
args = parser.parse_args()

result_dir =  args.dir
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

def Send_Handler(s, addr):
    send_array = np.empty([10000, 2])
    seq_num = 0
    while True:
        stamp = time.time()
        send_array[seq_num] = [seq_num, stamp]
        message = "{},{}".format(seq_num, stamp)
        print("send,"+message)
        s.sendto(message.encode('utf-8'), addr)
        pause = stamp+0.02-time.time()
        seq_num += 1
        if pause > 0:
            time.sleep(pause)
        if seq_num == 10000:
            break
    columns = ['seq_no', 'send_time']
    df = pd.DataFrame(send_array, columns=columns)
    df.to_pickle(result_dir + "/udp_host_send.pkl")

def Recv_Handler(s):
    rec_array = np.empty([10000, 2])
    count = 0
    while True:
        data, addr = s.recvfrom(4096)
        data = data.decode('utf-8')
        count += 1
        stamp = time.time()
        print(data)
        try:
            seq, _ = str(data).split(",")
            ind = int(seq)
            rec_array[ind] = [ind, stamp]
        except:
            pass
        if count == 10000:
            break
    columns = ['seq_no', 'rec_time']
    df = pd.DataFrame(rec_array, columns=columns)
    df.to_pickle(result_dir + "/udp_host_rec.pkl")

def Main():
    host = "130.235.202.199"
    # host = "130.235.202.201"
    # port = 12345
    port = 31234
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
