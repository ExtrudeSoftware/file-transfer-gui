import socket     
import time
import random

class Packet:
    def __init__(self, data, seqnum):
        self.data = data
        self.seqnum = seqnum

class Client:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.alive = True
    
    def connect(self):
        self.s.connect((self.host, self.port))

    def send(self, payload):
        self.s.send(payload.encode())
    
    def sendbytes(self, payload):
        self.s.send(payload)
    
    def recv(self):
        return self.s.recv(1024).decode()

    def close(self):
        self.s.close()

class SAWClient(Client):
    def setup(self):
        self.s.settimeout(0.5)

    def send_file(self, buffer, rnumber):
        packets = []
        with open("DataSent.txt", "rb") as f:
            seqnum = 0
            while True:
                data = f.read(buffer)
                packets.append(Packet(data, seqnum))
                if not data:
                    break
                seqnum += 1

        self.units = 1
        self.lost = 0
        start = time.time()

        i = 0
        while i < len(packets) - 1:
            try:
                if self.recv() == "ack":
                    continue
            except socket.timeout:
                if random.randint(0, 99) < rnumber:
                    self.lost += 1
                else:
                    self.sendbytes(packets[i].data)
                    self.units += 1
            i += 1
        
        end = time.time()
        self.send(f"###TRANSMISSION INFO###;TIME={end - start};UNITS={self.units};LOST={self.lost}")

class GBNClient(Client):
    def setup(self):
        self.s.settimeout(1)

    def send_file(self, buffer, rnumber, window_size):
        packets = []
        with open("DataSent.txt", "rb") as f:
            seqnum = 0
            while True:
                data = f.read(buffer)
                packets.append(Packet(data, seqnum))
                if not data:
                    break
                seqnum += 1

        self.units = 1
        self.lost = 0
        start = time.time()

        base = 0
        while base < len(packets) - 1:
            for p in packets[base:base+window_size]:
                if random.randint(0, 99) < rnumber:
                    self.lost += 1
                else:
                    self.send(f"{p.seqnum} {p.data.decode()}")
                    self.units += 1

            try:
                self.recv()
            except socket.timeout:
                for p in packets[base:base+window_size]:
                    self.send(f"{p.seqnum} {p.data.decode()}")
                break

            base += 1
        
        end = time.time()
        self.send(f"###TRANSMISSION INFO###;TIME={end - start};UNITS={self.units};LOST={self.lost}")

if __name__ == "__main__":
    sc = GBNClient("192.168.0.30", 3131)
    sc.setup()
    sc.connect()
    sc.send_file(10, -1, 4)