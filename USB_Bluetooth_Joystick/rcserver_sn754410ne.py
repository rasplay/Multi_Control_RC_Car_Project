import socket
import sys
import RPi.GPIO as gpio
import time

HOST = '192.168.0.6' # RCÄ« ¶óÁîº£¸®ÆÄÀÌ IP°ªÀ¸·Î º¯°æÇÊ¿ä.
PORT = 10000
TIME_OUT = 100

#Motor 1 Enable GPIO Pin
IC12EN = 23

#Motor 2 Enable GPIO Pin
IC34EN = 24

#Motor 1 GPIO Pin
IC1A = 28
IC2A = 31

#Motor 2 GPIO Pin
IC3A = 29
IC4A = 30

gpio.cleanup()

gpio.setmode(gpio.BCM)

#Motor 1,2 Enable
gpio.setup(IC12EN, gpio.OUT)
gpio.output(IC12EN, gpio.LOW)
gpio.setup(IC34EN, gpio.OUT)
gpio.output(IC34EN, gpio.LOW)

#Motor Pin Setup
gpio.setup(IC1A, gpio.OUT)
gpio.setup(IC2A, gpio.OUT)
gpio.setup(IC3A, gpio.OUT)
gpio.setup(IC4A, gpio.OUT)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (HOST, PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

def main():
    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()

        # Timeout
        connection.settimeout(TIME_OUT)

        try:
            print >>sys.stderr, 'connection from', client_address

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print >>sys.stderr, 'received "%s"' % data

                if data:
                    pdata = parsing_data(data)
                    print 'Go %s' % pdata

                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break

        except socket.timeout:
            print 'timeout error : "%d" secs' % TIME_OUT
            connection.close()

        finally:
            # Clean up the connection
            connection.close()

def parsing_data(data) :
    data = data.lower()
    print 'receive data : %s' % data

    try:
        intindex = data.index("rcpi")
        getStr = data.replace("rcpi","")
        getStr = getStr.strip()
        print >>sys.stderr, 'Receive Key : "%s"' % getStr

        if ( getStr == 'ff' ):
            print 'Move Forward / "%d" speed'
        elif ( getStr == 'bb' ):
            print 'Move Backward / "%d" speed'
        elif ( getStr == 'll' ):
            print 'Turn Left'
        elif ( getStr == 'rr' ):
            print 'Turn Right'
        elif ( getStr == 'bf' ):
            print 'stop For/Backward'
        elif ( getStr == 'rl' ):
            print 'stop Left/Right'
        elif ( getStr == 'ee' ):
            print 'toggle Motor Enable'
        elif ( getStr == 'dd' ):
            print 'toggle Motor Disable'
        else:
            print 'unknown commend'
            return 'u'

        run_motor(getStr)

    except ValueError:
        return 'a'

def run_motor(rcvStr):
    if ( rcvStr == 'rr' ):
        print 'GPIO Turn Right'
        gpio.output(IC1A, gpio.LOW)
        gpio.output(IC2A, gpio.HIGH)
    elif ( rcvStr == 'll' ):
        print 'GPIO Turn Left'
        gpio.output(IC1A, gpio.HIGH)
        gpio.output(IC2A, gpio.LOW)
    elif ( rcvStr == 'rl' ):
        print 'GPIO Front Wheel Zero'
        gpio.output(IC1A, gpio.LOW)
        gpio.output(IC2A, gpio.LOW)
    elif ( rcvStr == 'ff' ):
        print 'GPIO Forward'
        gpio.output(IC3A, gpio.LOW)
        gpio.output(IC4A, gpio.HIGH)
    elif ( rcvStr == 'bb' ):
        print 'GPIO Backward'
        gpio.output(IC3A, gpio.HIGH)
        gpio.output(IC4A, gpio.LOW)
    elif ( rcvStr == 'bf' ):
        print 'GPIO Stop Back Wheel'
        gpio.output(IC3A, gpio.LOW)
        gpio.output(IC4A, gpio.LOW)
    elif ( rcvStr == 'ee' ):
        print 'Motor Enable'
        gpio.output(IC12EN, gpio.HIGH)
        gpio.output(IC34EN, gpio.HIGH)
    elif ( rcvStr == 'dd' ):
        print 'Motor Disable'
        gpio.output(IC12EN, gpio.LOW)
        gpio.output(IC34EN, gpio.LOW)

if __name__ == "__main__":
    main()
