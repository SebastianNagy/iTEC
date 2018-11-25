#!/usr/bin/python
# view_rows.py - Fetch and display the rows from a MySQL database query
# import the MySQLdb and sys modules
import RPi.GPIO as GPIO # always needed with RPi.GPIO 
import MySQLdb
import sys
import os
import copy
import time
import math

import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

#Creez obiect din clasa MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

#Caut cartele. Daca una e aproape, o scanez
while continue_reading:
    
    #Scanez dupa carduri 
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    #Dacaam gasit
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    #Iau UID
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    #Daca am UID
    if status == MIFAREReader.MI_OK:

        # Print UID
        #print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
    	buf = "%02X%02X%02X%02X" % (uid[0], uid[1], uid[2], uid[3])
        print buf
	if buf == "6C1559A3":
		print("card bun")
		break;


GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT) #PWM SF
GPIO.setup(13,GPIO.OUT) #PWM SS
GPIO.setup(18,GPIO.OUT) #PWM DF
GPIO.setup(19,GPIO.OUT) #PWM DS

GPIO.setup(17,GPIO.OUT) #SF IM1
GPIO.setup(27,GPIO.OUT) #SF IM2
GPIO.output(17,1)
GPIO.output(27,0)

GPIO.setup(22,GPIO.OUT) #SS IM3
GPIO.setup(20,GPIO.OUT) #SS IM4
GPIO.output(22,1)
GPIO.output(20,0)

GPIO.setup(5,GPIO.OUT) #DF IM1
GPIO.setup(6,GPIO.OUT) #DF IM2
GPIO.output(5,1)
GPIO.output(6,0)

GPIO.setup(26,GPIO.OUT) #DS IM3
GPIO.setup(16,GPIO.OUT) #DS IM4
GPIO.output(26,1)
GPIO.output(16,0)

pSF=GPIO.PWM(12,100)
pSS=GPIO.PWM(13,100)
pDF=GPIO.PWM(18,100)
pDS=GPIO.PWM(19,100)


connection = MySQLdb.connect (host = "localhost", user = "itec", passwd = "cmfsebi", db = "scriecoord")

cursor = connection.cursor ()

cursor.execute ("SELECT * FROM scriecoord")

data = cursor.fetchall()
for row in data :
    row[0]

i=0
n=0
k=0
total =0
mylist=[]
vec=[]
vec.append(0)
mylist=copy.deepcopy(row[0])
print (mylist)


for word in mylist:
    total+=len(word)

while mylist[i]!=';':
    n=n*10+int(mylist[i])
    i+=1
for j in range(i+1,total-1):
    if (mylist[j]==';'):
        vec.append(0)
    else:
     if (mylist[j]==','):
        vec.append(0)        
        k+=1
	if (vec[k] == 0 and vec[k-1] == 0):
		k-=1
     else:
        m=int(mylist[j])
        vec[k]=vec[k]*10+m


#xorig=vec[0]
#yorig=vec[1]
xorig=0;
yorig=0;

k=k- k%3
i=0;

print (vec) #this is vec with good stuff

def meidrept(t):
	print("C point is on line\n")
	GPIO.output(5,0)
	GPIO.output(6,1)
	GPIO.output(26,0)
	GPIO.output(16,1)
	GPIO.output(22,0)
	GPIO.output(20,1)
	GPIO.output(17,0)
	GPIO.output(27,1)
	pSF.start(100)
	pSS.start(100)
	pDF.start(100)
	pDS.start(100)
	time.sleep(t)
def meistanga(unghi):
	print("C point is on the left side of AB (turn left)\n")
	GPIO.output(5,1)
	GPIO.output(6,0)
	GPIO.output(26,1)
	GPIO.output(16,0)

	GPIO.output(22,0)
	GPIO.output(20,1)
	GPIO.output(17,0)
	GPIO.output(27,1)
	pSF.start(100)
	pSS.start(100)
	pDF.start(100)
	pDS.start(100)
	if (180 - unghi < 25):
		time.sleep(0.1*math.fabs(unghi)/90)
	else:
		time.sleep (0.7*math.fabs(unghi)/90)

def meidreapta(unghi):
	print("C point is on the right side of AB (turn right)\n")
	GPIO.output(5,0)
	GPIO.output(6,1)
	GPIO.output(26,0)
	GPIO.output(16,1)

	GPIO.output(22,1)
	GPIO.output(20,0)
	GPIO.output(17,1)
	GPIO.output(27,0)

	pSF.start(100)
	pSS.start(100)
	pDF.start(100)
	pDS.start(100)
	if (180 - unghi < 25):
		time.sleep(0.1*math.fabs(unghi)/90)
	else:
		time.sleep (0.7*math.fabs(unghi)/90)

for j in range (0, k-1, 4):
	print(vec[j], vec[j+1], vec[j+2], vec[j+3], vec[j+4], vec[j+5])
	R1=(vec[j+2]-vec[j])*(vec[j+5] - vec[j+1])
	R=(vec[j+2]-vec[j])*(vec[j+3] - vec[j+1])
	R2=(vec[j+2]-vec[j+4])*(vec[j+3]-vec[j+1])
	valr=R-R1-R2

	a = math.sqrt((vec[j+2] - vec[j+4])**2 +(vec[j+3] - vec[j+5])**2)
	c = math.sqrt((vec[j] - vec[j+2])**2 + (vec[j+1] - vec[j+3])**2)
	b = math.sqrt((vec[j] - vec[j+4] )**2 + (vec[j+1] - vec[j+5])**2)
	#print(round((a**2 + c**2 -b**2)/(2*a*c)),3)
	if (a*c != 0):
		unghi = math.acos(round((a**2 + c**2 -b**2)/(2*a*c),10))*57.3
		print(unghi)
    	
		if ((valr > (-0.05)) and (valr < 0.05)):
			meidrept(0.15)
		else:
			if (valr > 0):
				meistanga(unghi)
				
			else:
				if (valr < 0):
					meidreapta(unghi)

GPIO.cleanup()
