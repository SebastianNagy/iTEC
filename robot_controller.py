#This is a simple python script to move a raspberry pi robot using WiFi
#For Complete Tutorial, visit http://rootsaid.com/robot-control-over-wifi/

import RPi.GPIO as GPIO
import socket
import csv
import time
import subprocess
import os
from ball_tracking import main
from YoloV2NCS.ncdsk import main2
python3_command = "ball_tracking.py" 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT) #PWM SF
GPIO.setup(13,GPIO.OUT) #PWM SS
GPIO.setup(18,GPIO.OUT) #PWM DF
GPIO.setup(19,GPIO.OUT) #PWM DS

GPIO.setup(17,GPIO.OUT) #SF IM1
GPIO.setup(27,GPIO.OUT) #SF IM2
GPIO.setup(22,GPIO.OUT) #SS IM3
GPIO.setup(20,GPIO.OUT) #SS IM4

GPIO.setup(5,GPIO.OUT) #DF IM1
GPIO.setup(6,GPIO.OUT) #DF IM2

GPIO.setup(26,GPIO.OUT) #DS IM3
GPIO.setup(16,GPIO.OUT) #DS IM4

pSF=GPIO.PWM(12,100)
pSS=GPIO.PWM(13,100)
pDF=GPIO.PWM(18,100)
pDS=GPIO.PWM(19,100)
UDP_IP = "0.0.0.0"
UDP_PORT = 5050

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))
GPIO.output(17,0)
GPIO.output(27,0)
#SS
GPIO.output(22,0)
GPIO.output(20,0)
#DF
GPIO.output(5,0)
GPIO.output(6,0)
#DS
GPIO.output(26,0)
GPIO.output(16,0)
pSF.start(100)
pSS.start(100)
pDF.start(100)
pDS.start(100)
aux=True;
while aux==True:
	data, addr = sock.recvfrom(1024)
	raw=data
	#print(type(data)) 
	raw2=data.decode("ascii")
	#print (raw2, type(raw2))
	print(raw2)
	if raw2=="forward":
		#SF
		GPIO.output(17,0)
		GPIO.output(27,1)
		#SS
		GPIO.output(22,0)
		GPIO.output(20,1)
		#DF
		GPIO.output(5,0)
		GPIO.output(6,1)
		#DS
		GPIO.output(26,0)
		GPIO.output(16,1)
		
		time.sleep(0.1)
		print ("Robot Move Forward")
	  
	  
	elif raw2=="stop":
		#SF
		GPIO.output(17,0)
		GPIO.output(27,0)
		#SS
		GPIO.output(22,0)
		GPIO.output(20,0)
		#DF
		GPIO.output(5,0)
		GPIO.output(6,0)
		#DS
		GPIO.output(26,0)
		GPIO.output(16,0)
		time.sleep(0.1)
		print ("Robot Stop")
	    

	elif raw2=="backward":
		#SF
		GPIO.output(17,1)
		GPIO.output(27,0)
		#SS
		GPIO.output(22,1)
		GPIO.output(20,0)
		#DF
		GPIO.output(5,1)
		GPIO.output(6,0)
		#DS
		GPIO.output(26,1)
		GPIO.output(16,0)
		time.sleep(0.1)
		print ("Robot Move Backward")

	elif raw2=="left":
		
		#SF
		GPIO.output(17,0)
		GPIO.output(27,1)
		#SS
		GPIO.output(22,0)
		GPIO.output(20,1)
		#DF
		GPIO.output(5,0)
		GPIO.output(6,0)
		#DS
		GPIO.output(26,0)
		GPIO.output(16,0)	
		time.sleep(0.1)
		print ("Robot Move Right")
	elif raw2=="right":

		#SF
		GPIO.output(17,0)
		GPIO.output(27,0)
		#SS
		GPIO.output(22,0)
		GPIO.output(20,0)
		#DF
		GPIO.output(5,0)
		GPIO.output(6,1)
		#DS
		GPIO.output(26,0)
		GPIO.output(16,1)
		time.sleep(0.1)
		print ("Robot Move Left")

	elif raw2=="action 1":
		aux=False
	elif raw2=="action2":
		#exec(open("ball_tracking.py").read())
		#os.system("sudo python3 ball_tracking.py")
		#output, error = process.communicate()
		main()
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(12,GPIO.OUT) #PWM SF
		GPIO.setup(13,GPIO.OUT) #PWM SS
		GPIO.setup(18,GPIO.OUT) #PWM DF
		GPIO.setup(19,GPIO.OUT) #PWM DS

		GPIO.setup(17,GPIO.OUT) #SF IM1
		GPIO.setup(27,GPIO.OUT) #SF IM2
		GPIO.setup(22,GPIO.OUT) #SS IM3
		GPIO.setup(20,GPIO.OUT) #SS IM4

		GPIO.setup(5,GPIO.OUT) #DF IM1
		GPIO.setup(6,GPIO.OUT) #DF IM2

		GPIO.setup(26,GPIO.OUT) #DS IM3
		GPIO.setup(16,GPIO.OUT) #DS IM4

		pSF=GPIO.PWM(12,100)
		pSS=GPIO.PWM(13,100)
		pDF=GPIO.PWM(18,100)
		pDS=GPIO.PWM(19,100)
		pSF.start(100)
		pSS.start(100)
		pDF.start(100)
		pDS.start(100)
	elif raw2=="device1on":
		main2()

GPIO.cleanup()
