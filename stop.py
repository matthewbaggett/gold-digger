# Import GPIO  
import RPi.GPIO as GPIO  
   
# Import sleep  
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
TurretEnable = 16
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
 

# Stop the Track by 'turning off' the enable GPIO pin  
GPIO.output(Track1Enable,GPIO.LOW)
GPIO.output(Track2Enable,GPIO.LOW)  
GPIO.output(TurretEnable,GPIO.LOW)
GPIO.output(BucketEnable,GPIO.LOW)  
 
# Always end this script by cleaning the GPIO  
GPIO.cleanup()  
