import cv2
from picamera2 import Picamera2
import numpy as np
from itertools import groupby
import math
from time import sleep
#----------------------------------------

def runs(difference):
    start = None
    def inner(n):
        nonlocal start
        if start is None:
            start = n
        elif abs(start-n) > difference:
            start = n
        return start
    return inner

#----------------------------------------
picam2 = Picamera2()
picam2.start()
while True:
	image = picam2.capture_array()
	greyFrame = image

	edges = cv2.Canny(greyFrame,50,150,apertureSize = 3)
	lines = cv2.HoughLines(edges,1,np.pi/180,200)
	if lines is not None and lines.size > 0:
		l = []
		angles = []
		for line in lines:
			rho,theta = line[0]
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))
			
			if (x2-x1)>0:
				slopeOfLine = (y2-y1)/(x2-x1)
			else:
				if y2-y1 > 0:
					slopeOfLine = float('inf')
				else:
					slopeOfLine = float('-inf')
			
			angles.append(math.degrees(math.atan(slopeOfLine)))
			
			l.append([x1, y1, x2, y2, slopeOfLine])
			cv2.line(greyFrame,(x1,y1),(x2,y2),(100,0,100),2)
		
		angles.sort()	
		angles = [next(g) for k, g in groupby(angles, runs(6))]
		
		'''
		depending on the diff b/w angles adjust speed.
		since we will have more angkes, smoother the turn. Maybe pick the rightmost and left most angles
		'''
		
		speed = 100 - 0.66*abs(angles[-1] - angles[0])
		
		
		print(angles, speed)
		if(len(angles) > 1):
			sleep(0.5)
			
		print("----------------------")
		
	cv2.imshow("Frame", image)

	if(cv2.waitKey(1) == ord("q")):
	  break

cv2.destroyAllWindows()
