import ast
import socket
from threading import Thread
from . import Settings

# ---------------------------------------------------------------------------
# Passive Module Class
# ---------------------------------------------------------------------------


class PassiveReceptor (Thread):
    # init method
    def __init__(self, data):
        # initializes the communication receiver module
        Thread.__init__(self)
        self.HOST = Settings.SELF_IP
        self.PORT = 61666
        self.data = data

    # connection method
    def connection(self, conn):
        # thread-isolated communicator (concurrent execution)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            self.decoder(data)
        conn.close()

    # decoder method
    def decoder(self, data):
        # check received communication
        segment = data.decode("utf-8")
        data = ast.literal_eval(segment)
        self.data.addJson(data)

    # run method
    def run(self):
        # start the PassiveReceiver master thread
        print("P. M. Actived")
        pm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        params = (self.HOST, self.PORT)
        pm_socket.bind(params)
        pm_socket.listen(5)
        while True:
            conn, attr = pm_socket.accept()
            connect = Thread(target=self.connection, args=(conn,))
            connect.start()
        pm_socket.close()
