# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import RPi.GPIO as GPIO # always needed with RPi.GPIO 
def main():
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

	pSF.start(0)
	pSS.start(0)
	pDF.start(0)
	pDS.start(0)
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help="path to the (optional) video file")
	ap.add_argument("-b", "--buffer", type=int, default=64,
		help="max buffer size")
	args = vars(ap.parse_args())

	#Definim limitele superioare/inferioare ale obiectului verde urmarit, initializam vectorul de puncte urmarite
	greenLower = (29, 86, 6)
	greenUpper = (64, 255, 255)
	pts = deque(maxlen=args["buffer"])
	 
	#Daca nu am primit video input -> webcam
	if not args.get("video", False):
		vs = VideoStream(src=0).start()
	 
	#Altfel, video
	else:
		vs = cv2.VideoCapture(args["video"])
	 
	#Da-i ragaz
	time.sleep(2.0)
	numarator=0
	# keep looping
	while (True):
		#Frameul curent
		frame = vs.read()
	 
		#Prelucram Frameul
		frame = frame[1] if args.get("video", False) else frame
	 
		#Daca am luat video si nu avem frame -> am ajuns la sfarsit
		if frame is None:
			break
	 
		#Modificam dimensiunea frameului, il bluram, il trecem in HSV color space
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	 
		#Construim o masca pentru culoarea verde si apoi eliminam bloburile
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		#Cautam conture in masca si initializam (x,y) ca si centrul mingii
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		center = None
	 
		#Continuam doar daca am gasit conture
		if len(cnts) > 0:
			#Cautam cel mai mare contur si apoi facem cel mai mic cerc
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	 
			if radius > 10:
				#Deseneaza cercul si punctele urmarite, si apoi initializeaza centrul
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
	 		        #print ("x=%d" %(x))
				print ("x="+str(x))
				print ("y="+str(y))
				print ("r="+str(radius))
				if (x < 200):
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
					time.sleep(0.3)
					pSF.start(0)
					pSS.start(0)
					pDF.start(0)
					pDS.start(0)
				elif (x> 400):
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
					time.sleep(0.3)
					pSF.start(0)
					pSS.start(0)
					pDF.start(0)
					pDS.start(0)
				if (radius > 80):
					if (radius >250):
						numarator+=1;
						print("NUMARATOR",numarator)
					if(numarator >= 5):
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
						time.sleep(1.5)
						pSF.start(0)
						pSS.start(0)
						pDF.start(0)
						pDS.start(0)
						#sys.exit(0)
					else:
						GPIO.output(5,1)
						GPIO.output(6,0)
						GPIO.output(26,1)
						GPIO.output(16,0)
						GPIO.output(22,1)
						GPIO.output(20,0)
						GPIO.output(17,1)
						GPIO.output(27,0)
						pSF.start(100)
						pSS.start(100)
						pDF.start(100)
						pDS.start(100)
						time.sleep(0.3)
						pSF.start(0)
						pSS.start(0)
						pDF.start(0)
						pDS.start(0)
				elif (radius < 40):
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
					time.sleep(0.3)
					pSF.start(0)
					pSS.start(0)
					pDF.start(0)
					pDS.start(0)
			
		#Vectorul de puncte marit
		pts.appendleft(center)
	
	
		# loop over the set of tracked points
		for i in range(1, len(pts)):
			#Daca vreun punct 
			if pts[i - 1] is None or pts[i] is None:
				continue
	 
			#Deseneaza liniile care unesc
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	 
		#Show the frame
		#cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	 
		if numarator >= 5:	
			break
	 
	#Daca nu folosim input video, oprim camera
	if not args.get("video", False):
		vs.stop()
	 
	#Altfel, eliberam camera
	else:
		vs.release()
	 
	#Inchide camera
	cv2.destroyAllWindows()
	GPIO.cleanup()
if (__name__=='__main__'):
	main()

