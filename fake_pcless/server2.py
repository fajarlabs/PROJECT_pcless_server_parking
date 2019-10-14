import multiprocessing
import socket
import time

"""
AUTHOR : Fajarlabs
WHATSAPP : 089663159652
"""

HOST = "0.0.0.0"
PORT = 5001


def handle(connection, address):

    try:
        while True:
            data = connection.recv(1024).decode('CP1252')
            sendData = data #+ ' server time {}'.format(time.time())
            connection.sendall(sendData.encode('CP1252'))
    except:
        pass
    finally:
        connection.close()


class Server(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            print("wait...")
            conn, address = self.socket.accept()
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()


if __name__ == "__main__":
    server = Server(HOST, PORT)
    try:
        print ('start')
        server.start()
    except:
        print ('something wrong happened, a keyboard break ?')
    finally:
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()
    print ('Goodbye')