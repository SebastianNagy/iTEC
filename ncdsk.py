import time
import os

def main2():
	timestr = time.strftime("%Y%m%d-%H%M%S.jpg")
	print( "YoloV2NCS/data/"+ timestr)
	os.system("raspistill -w 640 -h 480 -o " + "YoloV2NCS/data/" + timestr)
	print("Raspistill ")
	os.system("python3 ./YoloV2NCS/detectionExample/Main.py --image ./YoloV2NCS/data/"+timestr)
	print("Generate done.")
if (__name__=='__main__'):
	main2()
