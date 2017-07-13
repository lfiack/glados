"""
Probe Window Manager
"""

import Image
import ImageOps

import cv2  
import numpy as np

class Probe:
    def __init__(self):
        print("Init Probe")
        self.noviceTemplate = cv2.imread("data/probe_novice_plex.png")
#        self.smallTemplate = cv2.imread("data/probe_small_plex.png")
        self.mediumTemplate = cv2.imread("data/probe_medium_plex.png")
        self.largeTemplate = cv2.imread("data/probe_large_plex.png")

    def compute(self,im):
#        im = self.keepColor(im)
        cvImage = np.array(im)
        novices = self.findPlex(cvImage,self.noviceTemplate)
#        smalls = self.findPlex(cvImage,self.smallTemplate)
        mediums = self.findPlex(cvImage,self.mediumTemplate)
        larges = self.findPlex(cvImage,self.largeTemplate)
        for pt in novices:  # Switch collumns and rows
            print ("Novice in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
#        for pt in smalls:  # Switch collumns and rows
#            print ("Small in " + str(pt[0]) + "," + str(pt[1]))
#            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (0, 255, 0), 2)
        for pt in mediums:  # Switch collumns and rows
            print ("Medium in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (0, 0, 255), 2)
        for pt in larges:  # Switch collumns and rows
            print ("Large in " + str(pt[0]) + "," + str(pt[1]))
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 255), 2)

        im = Image.fromarray(cvImage)
        return im

    def findPlex(self,im,template):
        res = cv2.matchTemplate(im,template,cv2.TM_CCOEFF_NORMED)  
        threshold = .8
        loc = np.where(res >= threshold)
        return zip(*loc[::-1])

    def keepColor(self, im):
        pixels = im.load()
        for i in range(im.size[0]): # for every pixel:
            for j in range(im.size[1]):
                if ((pixels[i,j][0] <= 150) or (pixels[i,j][1] <= 150) or (pixels[i,j][2] <= 150)):
                    pixels[i,j] = (0, 0 ,0)
        return im

class Plex:
    def __init__(self,size):
        print("Init " + size + " Plex")
        self.size = size
