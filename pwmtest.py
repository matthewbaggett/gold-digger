# Import GPIO  
import RPi.GPIO as GPIO  
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import SimpleHTTPServer
import SocketServer
import thread
from time import sleep  
 
# Set the GPIO mode  
GPIO.setmode(GPIO.BCM)
 
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

p = GPIO.PWM(Track1Enable,50)
p.start(50)

sleep(5)
p.stop()

GPIO.cleanup()
