import ast
import socket
from .Sender import ActiveSender
from . import Settings
from threading import Thread

# ---------------------------------------------------------------------------
# Master Receiver Class
# ---------------------------------------------------------------------------

class MasterReceptor (Thread):
    # init method
    def __init__(self):
        # initializes the communication receiver module
        Thread.__init__(self)
        self.HOST = Settings.SELF_IP
        self.PORT = 61667
        self.address_list = Settings.ADDRESS_LIST
        self.database = []

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
        self.process_data(data)

    # process_data method
    def process_data(self, json):
        # calculates the average of the times informed and returns them to the slaves
        self.database.append(json)
        if len(self.database) == len(self.address_list):
            hour = 0
            minute = 0
            second = 0
            for json in self.database:
                hour = hour + json['HOUR']
                minute = minute + json['MINUTE']
                second = second + json['SECOND']
            hour = round(hour / len(self.address_list))
            minute = round(minute / len(self.address_list))
            second = round(second / len(self.address_list))
            time_dict = {'HOUR': hour,
                         'MINUTE': minute,
                         'SECOND': second}
            threads = []
            for address in self.address_list:
                send = ActiveSender(time_dict, address, 61666)
                threads.append(send)
                send.start()
            for thread in threads:
                thread.join()
            self.database.clear()

    # run method
    def run(self):
        # start the MasterReceiver master thread
        print("M. R. Actived")
        pm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        params = (self.HOST, self.PORT)
        pm_socket.bind(params)
        pm_socket.listen(5)
        while True:
            conn, attr = pm_socket.accept()
            connect = Thread(target=self.connection, args=(conn,))
            connect.start()
        pm_socket.close()
