import cv2  
import numpy as np

def findTemplate(im,template):
    res = cv2.matchTemplate(im,template,cv2.TM_CCOEFF_NORMED)  
    threshold = .8
    loc = np.where(res >= threshold)
    return zip(*loc[::-1])
