import cv2  
import numpy as np

def findTemplate(im,template):
    res = cv2.matchTemplate(im,template,cv2.TM_CCOEFF_NORMED)  
    threshold = .85
    loc = np.where(res >= threshold)
    return (res,zip(*loc[::-1]))

def isColorPresent(im,colorCode,tolerance):
    """
    Return True if a color is present in an image
    im is the input image
    colorCode is a 3-tuple that contains th RGB value of the color to detect
    tolerance is the acceptable distance regarding the colorCode
    """
    for line in im:
        for pix in line:
            if isClose(pix[0],colorCode[0],tolerance) and isClose(pix[1],colorCode[1],tolerance) and isClose(pix[2],colorCode[2],tolerance):
                return True

    return False

def isClose(a,b,tol):
    return abs(a-b) <= tol
