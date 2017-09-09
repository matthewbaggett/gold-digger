#!/usr/bin/python
# Import GPIO  
import RPi.GPIO as GPIO  
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import SimpleHTTPServer
import SocketServer
import thread
from time import sleep  
 
# Set the GPIO mode  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
 
# Define GPIO pins  
Track1A = 27 
Track1B = 24 
Track1Enable = 5 
Track2A = 6
Track2B = 22
Track2Enable = 17
TurretA = 23
TurretB = 16
TurretEnable = 12
BucketA = 13
BucketB = 18
BucketEnable = 25

# Set up defined GPIO pins  
GPIO.setup(Track1A,GPIO.OUT)  
GPIO.setup(Track1B,GPIO.OUT)  
GPIO.setup(Track1Enable,GPIO.OUT)
GPIO.setup(Track2A,GPIO.OUT)  
GPIO.setup(Track2B,GPIO.OUT)  
GPIO.setup(Track2Enable,GPIO.OUT)
GPIO.setup(TurretA,GPIO.OUT)  
GPIO.setup(TurretB,GPIO.OUT)  
GPIO.setup(TurretEnable,GPIO.OUT)
GPIO.setup(BucketA,GPIO.OUT)  
GPIO.setup(BucketB,GPIO.OUT)  
GPIO.setup(BucketEnable,GPIO.OUT)

# Define operational constants
TestSleepInterval = 0.3
DefaultPWMDuty = 20
DefaultPWMFrequency = 50
PWMDutyDivisor = 0.9

# Setup PWM objects
pwmTrack1 = GPIO.PWM(Track1Enable,DefaultPWMFrequency)
pwmTrack2 = GPIO.PWM(Track2Enable,DefaultPWMFrequency)
pwmTurret = GPIO.PWM(TurretEnable,DefaultPWMFrequency)
pwmBucket = GPIO.PWM(BucketEnable,DefaultPWMFrequency)
 
# Make sure we're stopped
GPIO.output(Track1Enable,GPIO.LOW)
GPIO.output(Track2Enable,GPIO.LOW)  
GPIO.output(TurretEnable,GPIO.LOW)
GPIO.output(BucketEnable,GPIO.LOW)  

def right_forward(duty=DefaultPWMDuty):
    GPIO.output(Track1A, GPIO.LOW)
    GPIO.output(Track1B, GPIO.HIGH)
    pwmTrack1.start(duty * PWMDutyDivisor)

def right_backward(duty=DefaultPWMDuty):
    GPIO.output(Track1A, GPIO.HIGH)
    GPIO.output(Track1B, GPIO.LOW)
    pwmTrack1.start(duty * PWMDutyDivisor)

def left_forward(duty=DefaultPWMDuty):
    GPIO.output(Track2A, GPIO.HIGH)
    GPIO.output(Track2B, GPIO.LOW)
    pwmTrack2.start(duty * PWMDutyDivisor)

def left_backward(duty=DefaultPWMDuty):
    GPIO.output(Track2A, GPIO.LOW)
    GPIO.output(Track2B, GPIO.HIGH)
    pwmTrack2.start(duty * PWMDutyDivisor)

def track_stop():
    pwmTrack1.stop()
    pwmTrack2.stop()

def turret_cw(duty=DefaultPWMDuty):
    GPIO.output(TurretA, GPIO.HIGH)
    GPIO.output(TurretB, GPIO.LOW)
    pwmTurret.start(duty * PWMDutyDivisor)

def turret_ccw(duty=DefaultPWMDuty):
    GPIO.output(TurretA, GPIO.LOW)
    GPIO.output(TurretB, GPIO.HIGH)
    pwmTurret.start(duty * PWMDutyDivisor)

def turret_stop():
    pwmTurret.stop()
    
def bucket_up(duty=DefaultPWMDuty):
    GPIO.output(BucketA, GPIO.LOW)
    GPIO.output(BucketB, GPIO.HIGH)
    pwmBucket.start(duty * PWMDutyDivisor)
    
def bucket_down(duty=DefaultPWMDuty):
    GPIO.output(BucketA, GPIO.HIGH)
    GPIO.output(BucketB, GPIO.LOW)
    pwmBucket.start(duty * PWMDutyDivisor)
    
def bucket_stop():
    pwmBucket.stop();

def forward(duty=DefaultPWMDuty):
    right_forward(duty);
    left_forward(duty);

def backward(duty=DefaultPWMDuty):
    right_backward(duty);
    left_backward(duty);

def all_stop():
    turret_stop()
    track_stop();

class MotionHandler(WebSocket):

    def handleMessage(self):
        # echo message back to client
        #self.sendMessage(self.data)
        messages = self.data.split('\n');
        for message in messages:
            print ("Message Recieved: " + message);
            motion, duty = message.split(' ')
            print("Motion: " + motion + " Duty: " + duty);
            if motion == 'track_forward':
                forward(int(duty))
            if motion == 'track_backward':
                backward(int(duty))
            if motion == 'track_left':
                right_backward(int(duty))
                left_forward(int(duty))
            if motion == 'track_right':
                left_backward(int(duty))
                right_forward(int(duty))
            if motion == 'track_stop':
                track_stop()

            if motion == 'turret_left':
                turret_ccw(int(duty))
            if motion == 'turret_right':
                turret_cw(int(duty))
            if motion == 'turret_stop':
                turret_stop()
                
            if motion == 'bucket_up':
                bucket_up(int(duty))
            if motion == 'bucket_down':
                bucket_down(int(duty))
            if motion == 'bucket_stop':
                bucket_stop()
        
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


PORT_HTTP = 80
PORT_SOCKET = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT_HTTP), Handler)

print "Web Service at " + str(PORT_HTTP) + " and socket on " + str(PORT_SOCKET) + "."

socket_server = SimpleWebSocketServer('', PORT_SOCKET, MotionHandler)

def self_test():
    forward()
    sleep(TestSleepInterval)
    backward()
    sleep(TestSleepInterval)
    track_stop()

    turret_cw()
    sleep(TestSleepInterval*3)
    turret_ccw()
    sleep(TestSleepInterval*3)
    turret_stop()

    all_stop()

def start_socket_server(a):
    # Setup stuff here...
    socket_server.serveforever()

def start_http_server(a):
    # Setup stuff here...
    httpd.serve_forever()

# start the server in a background thread
thread.start_new_thread(start_socket_server,('',))
thread.start_new_thread(start_http_server,('',))

#self_test()

c = raw_input("Type something to quit.")

httpd.shutdown();

# Always end this script by cleaning the GPIO  
GPIO.cleanup()  
