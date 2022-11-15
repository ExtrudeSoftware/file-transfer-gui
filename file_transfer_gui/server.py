import socket
from threading import Thread

class Server:
    def __init__(self, port, psize):
        self.psize = psize # 1024 bytes (1 kb)
        self.port = port
        self.s = socket.socket()
        self.alive = True
        self.packets = []
    
    def setup(self):
        self.s.bind(("", self.port))
        self.s.listen(5)

    def send(self, c, payload):
        c.send(payload.encode())

    def recv(self, c, on_message):
        while self.alive:
            msg = c.recv(self.psize).decode()
            #if msg: Thread(target=on_message, args=(c, msg)).start()
            if msg: on_message(c, msg)

    def main_loop(self, on_connection, on_message):
        while self.alive:
            c, addr = self.s.accept()
            Thread(target=on_connection, args=(c, addr)).start()
            Thread(target=self.recv, args=(c, on_message)).start()

    def start(self, on_connection, on_message):
        # on_connection(c, addr)
        # on_message(c, msg)
        Thread(target=self.main_loop, args=(on_connection, on_message)).start()

class SAWServer(Server):
    def recv_file(self, c, msg):
        if msg.startswith("###TRANSMISSION INFO###"):
            msg = msg.split(";")[1:]
            for i in msg:
                d, v = i.split("=")
                if d == "TIME":
                    time = v
                elif d == "UNITS":
                    units = v
                elif d == "LOST":
                    lost = v
            
            with open("DataRecieved.txt", "w") as f:
                print(self.packets)
                f.write(f"Time: {time}\nUnits: {units}\nLost: {lost}\nData: " + "".join(self.packets))
                self.packets = []
        else:
            self.packets.append(msg)
            self.send(c, "ack")
    
    def start(self, on_connection):
        Thread(target=self.main_loop, args=(on_connection, self.recv_file)).start()

class GBNServer(Server):
    def setup(self, window_size):
        self.s.bind(("", self.port))
        self.s.listen(5)

        self.expected_num = 0

    def recv_file(self, c, msg):
        if msg.startswith("###TRANSMISSION INFO###"):
            msg = msg.split(";")[1:]
            for i in msg:
                d, v = i.split("=")
                if d == "TIME":
                    time = v
                elif d == "UNITS":
                    units = v
                elif d == "LOST":
                    lost = v
            
            with open("DataRecieved.txt", "w") as f:
                print(self.packets)
                f.write(f"Time: {time}\nUnits: {units}\nLost: {lost}\nData: " + "".join(self.packets))
                self.packets = []
        else:
            sn = msg.split(" ")[0]
            msg = "".join(msg.split(" ")[1:])[0:-1]
            self.packets.append(msg)
            if int(sn) == self.expected_num:
                self.send(c, "ack")
                self.expected_num += 1
            
    
    def start(self, on_connection):
        Thread(target=self.main_loop, args=(on_connection, self.recv_file)).start()

if __name__ == "__main__":
    ss = GBNServer(3131, 1024)
    ss.setup(4)
    ss.start(lambda x, y: print(x, y))