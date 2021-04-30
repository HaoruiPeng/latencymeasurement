import socket
from _thread import *
import threading
import time

print_lock = threading.Lock()

# thread function
def threaded(c):
    while True:
        data, addr = c.recvfrom(4096)
        if not data:
            pass
			# lock released on exit
            print_lock.release()
            break
        try:
            seq, stamp = data.decode('utf-8').split(",")
            message = "{},{}".format(seq, time.time())
            c.sendto(message.encode('utf-8'), addr)
        except:
            pass

	# connection closed
    c.close()

def Main():
    host = "0.0.0.0"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print("socket binded to port", port)

	# put the socket into listening mode
    # s.listen(5)
    # print("socket is listening")

	# a forever loop until client wants to exit
    while True:
        # establish connection with client
        # c, addr = s.accept()
		# lock acquired by client
        print_lock.acquire()
        # print('Connected to :', addr[0], ':', addr[1])
		# Start a new thread and return its identifier
        start_new_thread(threaded, (s,))
    s.close()

if __name__ == '__main__':
    Main()
