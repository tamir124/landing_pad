import threading
import serial
import time
import requests
import sys
import json
from UDP import UDP
from threading import Thread;


def ethernet():
    global c
    c = UDP("169.254.26.86","169.254.52.110",5005)
    Thread(target=receive).start()
    while True:
        a = input()
        c.transmit(a)

def receive():
    try:
        c.receive()
    except OSError:
        print("Is the ip accurate? Are you sure the first IP argument in constructor is this device ip? ")

if __name__ == '__main__':
    ethernet()
