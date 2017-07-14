"""
DScan Window Manager
"""

import Image
import ImageOps

import cv2  
import numpy as np

import vision

class Dscan:
    def __init__(self):
        print("Init Dscan")
        self.corvetteTemplate = cv2.imread("data/overview_corvette.png")
        self.frigateTemplate = cv2.imread("data/overview_frigate.png")
        self.destroyerTemplate = cv2.imread("data/overview_destroyer.png")

    def compute(self,im):
#        im = self.keepColor(im)
        cvImage = np.array(im)
        self.corvettes = vision.findTemplate(cvImage,self.corvetteTemplate)
        self.frigates = vision.findTemplate(cvImage,self.frigateTemplate)
        self.destroyers= vision.findTemplate(cvImage,self.destroyerTemplate)
        for pt in self.corvettes:  # Switch collumns and rows
            print ("Corvette in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
        for pt in self.frigates:  # Switch collumns and rows
            print ("Frigate in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (0, 255, 0), 2)
        for pt in self.destroyers:  # Switch collumns and rows
            print ("Destroyer in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (0, 0, 255), 2)

        im = Image.fromarray(cvImage)
        return im

#    def keepColor(self, im):
#        pixels = im.load()
#        for i in range(im.size[0]): # for every pixel:
#            for j in range(im.size[1]):
#                if ((pixels[i,j][0] <= 150) or (pixels[i,j][1] <= 150) or (pixels[i,j][2] <= 150)):
#                    pixels[i,j] = (0, 0 ,0)
#        return im
