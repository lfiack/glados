"""
Reads and store the state of the Eve-online client
"""

import Image, ImageTk
import pyscreenshot as ImageGrab
import os
import operator
import re

import cv2  
import numpy as np

import logreader

import vision

class EveState():
    def __init__(self):
        print ("Init EveState")
        self.eveWindowList = []
        self.logsList = []
        self.logreader = logreader.LogReader()

    def addEveWindow(self, eveWindow):
        self.eveWindowList.append(eveWindow)

    def clearObjectLists(self):
        for w in self.eveWindowList:
            w.clearObjectList()

    def compute(self):
#        print("Compute")
        pilImage=ImageGrab.grab()

        # Read the logs
        self.logsList = []
        loop = True
        while loop:
            loop,s=self.logreader.read()
            if s:
                self.logsList.append(s)

        self.clearObjectLists()
        for w in self.eveWindowList:
            w.cropScreen(pilImage)
            cvImage = np.array(w.pilImage)

            for t in w.templateList:
                (res,items) = vision.findTemplate(cvImage,t[1])
                for pt in items:  # Switch collumns and rows
#                    print (t[0] + " in " + str(pt[0]) + "," + str(pt[1]))
                    cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
                    w.addObject(EveObject(t[0],pt,res[(pt[1],pt[0])]))

            w.pilImage = Image.fromarray(cvImage)

    def display(self):
        print "------------------------"
        print "Logs"
        for l in self.logsList:
            print l
        for w in self.eveWindowList:
            print "------------------------"
            print w.name + " from " + str(w.startPos) + " to " + str(w.endPos) + " contains :"
            for o in w.eveObjectList:
                print o.name + " in " + str(o.relativePos) + "(rel) ; " + str(tuple(map(operator.add, o.relativePos, w.startPos))) + "(abs) (" + str(o.res) + ")"

class EveWindow():
    def __init__(self, name, startPos, endPos):
        self.name = name
        self.startPos = startPos
        self.endPos = endPos
        self.eveObjectList = []
        self.pilImage = Image.new("RGB",tuple(map(operator.sub, self.endPos, self.startPos)),"black")
        self.path = os.environ['PWD'] + "/data/"
        self.templateList = []
#        print self.name
        for filename in os.listdir(self.path):
            winRE = "(?<=" + self.name + "_).*"
            winName = re.search(winRE, filename)
            if winName:
                winName = winName.group(0)
                winName = winName.split(".")[0]
                pathname=self.path+filename
                self.templateList.append((winName,cv2.imread(pathname)))
#                print "winName=" + winName
#                print "pathname=" + pathname

    def setPos(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

    def addObject(self,eveObject):
        self.eveObjectList.append(eveObject)

    def clearObjectList(self):
        self.eveObjectList = []

    def cropScreen(self, pilImage):
        area = (self.startPos[0],self.startPos[1],self.endPos[0],self.endPos[1])
        self.pilImage = pilImage.crop(area)

class EveObject():
    def __init__(self, name, relativePos, res):
        self.name = name
        self.relativePos = relativePos
        self.res = res

# Test
if __name__ == '__main__':
    s = EveState()

    w = EveWindow("win1",(100,100),(200,200))
    o = EveObject("obj11",(15,15,1))
    w.addObject(o)
    o = EveObject("obj12",(30,30,1))
    w.addObject(o)
    s.addEveWindow(w)

    w = EveWindow("win2",(200,200),(300,300))
    o = EveObject("obj21",(45,45,1))
    w.addObject(o)
    o = EveObject("obj22",(60,60,1))
    w.addObject(o)
    s.addEveWindow(w)

    print "==================================="
    s.display()

    s.clearObjectLists()
    print "==================================="
    s.display()

    o = EveObject("obj13",(15,15,1))
    s.eveWindowList[0].addObject(o)
    o = EveObject("obj14",(30,30,1))
    s.eveWindowList[0].addObject(o)

    o = EveObject("obj23",(45,45,1))
    s.eveWindowList[1].addObject(o)
    o = EveObject("obj24",(60,60,1))
    s.eveWindowList[1].addObject(o)

    print "==================================="
    s.display()
