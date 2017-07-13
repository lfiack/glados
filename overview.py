"""
Overview Window Manager
"""

import Image
import ImageOps

import cv2  
import numpy as np

import vision

class Overview:
    def __init__(self):
        print("Init Overview")
        self.stationTemplate = cv2.imread("data/overview_station.png")
        self.accGateTemplate = cv2.imread("data/overview_acc_gate.png")

    def compute(self,im):
#        im = self.keepColor(im)
        cvImage = np.array(im)
        self.stations = vision.findTemplate(cvImage,self.stationTemplate)
        self.accGates = vision.findTemplate(cvImage,self.accGateTemplate)
        for pt in self.stations:  # Switch collumns and rows
            print ("Station in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
        for pt in self.accGates:  # Switch collumns and rows
            print ("Acceleration Gate in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (0, 255, 0), 2)

        im = Image.fromarray(cvImage)
        return im

#    def keepColor(self, im):
#        pixels = im.load()
#        for i in range(im.size[0]): # for every pixel:
#            for j in range(im.size[1]):
#                if ((pixels[i,j][0] <= 150) or (pixels[i,j][1] <= 150) or (pixels[i,j][2] <= 150)):
#                    pixels[i,j] = (0, 0 ,0)
#        return im
