#!/usr/bin/env python3


# based on tutorials:
#   http://www.roman10.net/serial-port-communication-in-python/
#   http://www.brettdangerfield.com/post/raspberrypi_tempature_monitor_project/

# Dependencies
# sudo apt-get install python3
# sudo apt-get install python3-pip
# NOT: sudo pip3 install serial!!!
# sudo pip3 install pyserial


import serial
import time
from threading import Timer

SERIALPORT1 = "/dev/ttyUSB0"
BAUDRATE1 = 1200

SERIALPORT2 = "/dev/ttyUSB1"
BAUDRATE2 = 1200


def startSerial(serPort, serBaudrate):
    print("INFO: starting serial port: %s on baudrate: %i" % (serPort, serBaudrate))
    
    try:
        ser = serial.Serial(serPort, serBaudrate)

    except Exception as e:
        print("ERROR: open serial port: " + str(e))
        exit()

    ser.bytesize = serial.EIGHTBITS    #number of bits per bytes
    ser.parity = serial.PARITY_NONE    #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = None     #block read
    ser.xonxoff = False    #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 0   #timeout for write
    
    return ser

def sendString(ser, message, intervalTime, cycleTotal, cycleCount):
    print("INFO: for serial port: %s in sendString interval: %i cycleTotal %i cycleCount %i" % (ser.name, intervalTime, cycleTotal, cycleCount))
    startTime = time.time()

    print(message)
    ser.write(message.encode())
    
    remainingTime = intervalTime - (time.time() - startTime)
    if remainingTime > 0:
        if cycleCount == cycleTotal:
           cycleCount = 0
        print("INFO: finished in sendString remaining time: %f" % (remainingTime))
        t = Timer(remainingTime, sendString, [ser, message, intervalTime, cycleTotal, cycleCount+1])
        t.start()
    else:
        print("ERROR: in sendString ramainingTime: %f is negative" %(remainingTime))



print("INFO: Starting Up Serial Monitor")
serArray = []
serArray.append(startSerial(SERIALPORT1, BAUDRATE1))
serArray.append(startSerial(SERIALPORT2, BAUDRATE2))

for ser in serArray:
    if ser.isOpen():
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output

            #ToDo Regelnummer toevoegen
            if ser.name == '/dev/ttyUSB0':
                #sendString(ser, "01                   12.64      \r\n\r\n", 5, 10, 1)
                sendString(ser, "time=1523612465000;sensor=standpijp;H=-97.42365cm;\r\n", 5, 5, 1)
            else:
                sendString(ser, "time=1523612465000;sensor=standpijp;H=-397.42365cm;\r\n", 5, 5, 1)
                
        except Exception as e:
            print("error communicating...: " + str(e))

    else:
        print("ERROR: cannot open serial port")

while True:
    print("INFO: In while True loop, do sleep, catch breaks...")
    time.sleep(20)
    #ToDo Catch break and cleanup
    #ToDo Stop threads+close serial ports
    #ser.close()
