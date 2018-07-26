import socket
import time


class UDP:
    sock1 = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP
    sock2 = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP
    
    def __init__(self,UDP_IP_PC,UDP_IP_RASP,port,):
        self.UDP_IP_PC = UDP_IP_PC
        self.UDP_IP_RASP = UDP_IP_RASP
        self.port = port
        


    def receive(self):
        self.sock1.bind((self.UDP_IP_PC, self.port))
        while True:
            data, addr = self.sock1.recvfrom(1024) # buffer size is 1024 bytes
            print (data.decode('utf-8'))
            
    def transmit(self,msg):
        self.sock2.sendto(msg.encode('utf-8'), (self.UDP_IP_RASP, self.port))



def transmit():
    while True:
        c.transmit("hello")
        time.sleep(1)

def receive():
    c.receive()








