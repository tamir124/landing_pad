import threading
import serial
import time
import requests
import sys
import json
from UDP import UDP
from threading import Thread;


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def sendSerial():
    global stop;
    if ser != 1:
        stop = False;
    else:
        stop = True;
    # c = input("Number of blinks (1-3): ");

    while stop != True:
        while True:
            try:
                c = int(input("enter 1-9: \n"))

            except ValueError:
                print("Input wasn't an integer, please try again.")
                continue
            break
        if c == 0:
            ser.write('0'.encode(encoding='UTF-8'))
        if c == 1:
            ser.write('1'.encode(encoding='UTF-8'));
        if c == 2:
            ser.write('2'.encode(encoding='UTF-8'));
        if c == 3:
            ser.write('3'.encode(encoding='UTF-8'));
        if c == 4:
            ser.write('4'.encode(encoding='UTF-8'));
        if c == 5:
            ser.write('5'.encode(encoding='UTF-8'));
        if c == 6:
            ser.write('6'.encode(encoding='UTF-8'));
        if c == 7:
            ser.write('7'.encode(encoding='UTF-8'));
        if c == 8:
            ser.write('8'.encode(encoding='UTF-8'));
        if c == 9:
            ser.write('9'.encode(encoding='UTF-8'));
        if c < 0:
            stop = True


def readSerial():
    while (stop != True):
        if (ser.in_waiting > 0 and stop is False):
            update = ser.read().decode(encoding='UTF-8')
            #I'm not sure i need to reset input buffer, maybe better without it
            #ser.reset_input_buffer();
            #print("update value is(abs):" + update);
            if (update == '1'):
                print("Case closed");
            if (update == '2'):
                print("Case open");
            #if (update == '3'):
                #print("The update is 3");
            if (update == '4'):
                print("Holder closed");
            if (update == '5'):
                print("Holder opened");
            if (update == '8'):
                print("Initiated takeoff operation")
                #tells the server the number was recieved, so clear json state
                #requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',json={'state': 'tami'})
            if (update == '9'):
                print("Initiated landing operation")
                # tells the server the number was recieved, so clear json state
                #requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',json={'state': 'tami'})


def server():
    while stop != True:
        r = requests.get('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir')
        try:
            dict = json.loads(r.text)
            action = dict["state"]
        except ValueError:
            print("Value error, http request receives a non valid json")
            action="Error in json"
        try:
            if int(action) >= 0 and int(action) <= 9:
                ser.write(action.encode(encoding='UTF-8'))
                if action == '0':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiated open case'})
                if action == '1':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiate open case'})
                if action == '2':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiated close case'})
                if action == '3':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Received 3, nothing changed'})
                if action == '4':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiated open holder'})
                if action == '5':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiated close case'})
                if action == '6':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Received 6, nothing changed'})
                if action == '7':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiated move finger'})
                if action == '8':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiated takeoff'})
                if action == '9':
                    requests.post('https://3z5qhgprj8.execute-api.eu-central-1.amazonaws.com/api/tamir/set',
                                  json={'state': 'Initiated landing'})

        except ValueError:
            continue


if __name__ == '__main__':
    print("**You can always enter -1 to exit the program**");
    # Tries to get port untill a correct port received
    ser = None;
    while ser is None:
        try:
            print("List of available ports:", serial_ports())
            port = input("Press Enter for default port(first in list), or write a port from the list: ")
            if port == '-1':
                ser = 1
            else:
                if port is '0' or port is "":
                    try:
                        ser = serial.Serial(serial_ports()[0], 115200)
                    except IndexError:
                        print("No available port found, is the program already running?")
                else:
                    ser = serial.Serial(port, 115200)
        except IOError:
            print("Port name incorrect, please try again.")
    Thread(target=sendSerial).start()
    #Thread(target=readSerial).start()
    Thread(target=server).start()
