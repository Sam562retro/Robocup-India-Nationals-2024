import cv2
import numpy as np


print(cv2.__version__)
vid = cv2.VideoCapture(0) 

prevCircle = None
dist = lambda x1, x2, y1, y2: (x1-x2)**2+(y1-y2)**2

while(True): 
    ret, frame = vid.read() 
    if not ret: break
    
    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(greyFrame, (11,11), 0)

    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 0.5, 1, param1=10, param2=50, minRadius=1, maxRadius=50)

    if circles is not None:
        circles = np.int16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen=i
            if prevCircle is not None: 
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) == dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen=i
        
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (100, 10, 100), 3)
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (100, 20, 100),3)
        prevCircle = chosen



    cv2.imshow('show', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  

vid.release() 
cv2.destroyAllWindows() 