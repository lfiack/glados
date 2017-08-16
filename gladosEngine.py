import Image, ImageTk
import pyscreenshot as ImageGrab

import cv2  
import numpy as np

import os.path
from shutil import copyfile
from ast import literal_eval

from pymouse import PyMouse

import threading
import time

import fsm
import vision

class GladosEngine(threading.Thread):
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.pilImage=Image
        self.gui = gui

        self.botStarted = False
        self.anomCounter = 0

        self.mouse = PyMouse()

        self.text = ""

        self.fsm = fsm.StateMachine()

        self.forsaken_rally_point_template = cv2.imread("./data/Forsaken_Rally_Point.png")
        self.core_template = cv2.imread("./data/Core.png")
        self.mobile_tractor_template = cv2.imread("./data/Mobile_Tractor.png")
        # TODO Pointed
        self.allied_template = cv2.imread("./data/Allied.png")
        self.neutral_template = cv2.imread("./data/Neutral.png")
        self.red_template = cv2.imread("./data/Red.png")
        self.orange_template = cv2.imread("./data/Orange.png")

        #Read settings
        self.settings = {}
        path=os.environ['HOME'] + "/.glados"
        if os.path.isfile(path) == False:
            print "Creating " + path + " file"
            copyfile("./settings.txt", path)

        f=open(path,"r")
        lines=f.readlines()
        for l in lines:
            if l != '\n':
                ll = l.split()
                self.settings[ll[0]] = literal_eval(ll[1])
                print ll[0] + " " + str(ll[1])
                
        self.fsm.addState("Init", self.initHandler)
        self.fsm.addState("Check anom", self.checkAnomHandler)
        self.fsm.addState("Warping to anom", self.warpingToAnomHandler)
        self.fsm.addState("Launch drones", self.launchDronesHandler)
        self.fsm.addState("Wait wreck", self.waitWreckHandler)
        self.fsm.addState("Farming", self.farmingHandler)
        self.fsm.addState("Scoop drones", self.scoopDronesHandler)

        self.fsm.addState("Align", self.alignHandler)
        self.fsm.addState("Warp off", self.warpOffHandler)
        self.fsm.addState("Safe", self.safeHandler)

        self.fsm.setStart("Init")

        self.running = True

    def startBot(self):
        self.botStarted = True

    def stopBot(self):
        self.botStarted = False

    def resetBot(self,nextState):
        self.fsm.setStart(nextState)

    def rightClick(self,coordinates):
        self.gui.addText("Right click in " + str(coordinates[0]) + "," + str(coordinates[1]))
        self.mouse.move(coordinates[0],coordinates[1])
        time.sleep(0.1)
        self.mouse.press(coordinates[0],coordinates[1],button=2)
        time.sleep(0.15)
        self.mouse.release(coordinates[0],coordinates[1],button=2)
        time.sleep(0.5)

    def leftClick(self,coordinates):
        self.gui.addText("Left click in " + str(coordinates[0]) + "," + str(coordinates[1]))
        self.mouse.move(coordinates[0],coordinates[1])
        time.sleep(0.1)
        self.mouse.press(coordinates[0],coordinates[1],button=1)
        time.sleep(0.15)
        self.mouse.release(coordinates[0],coordinates[1],button=1)
        time.sleep(0.5)

    def move(self,coordinates):
        self.mouse.move(coordinates[0],coordinates[1])

    def checkLocal(self):
        image=ImageGrab.grab(bbox=self.settings["localBBox"])
        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.allied_template)
        if items:
            allied = len(items)
        else:
            allied = 0

        (res,items) = vision.findTemplate(cvImage,self.neutral_template)
        if items:
            neutral = len(items)
        else:
            neutral = 0

        (res,items) = vision.findTemplate(cvImage,self.red_template)
        if items:
            red = len(items)
        else:
            red = 0

        (res,items) = vision.findTemplate(cvImage,self.orange_template)
        if items:
            orange = len(items)
        else:
            orange = 0

        self.gui.addText (str(allied) + " allies, " + str(neutral) + " neutrals, " + str(orange) + " oranges, " + str(red) + " reds")

        if neutral or red:
            return True
        else:
            return False

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if self.botStarted:
                self.gui.resetText()
                self.gui.addText("=====================")
                self.gui.addText(time.strftime("%d/%m/%Y - %H:%M:%S"))
                self.gui.addText("Anomaly counter: " + str(self.anomCounter))
                self.pilImage=self.fsm.step()

                self.gui.logText()
            else:
                time.sleep(1)


    def initHandler(self):
        self.gui.addText("* Init state")
        # Cropping the probe scanner
        bbox=self.settings["probeBBox"]
        image=ImageGrab.grab(bbox=bbox)
        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.forsaken_rally_point_template)

        if self.checkLocal():
            self.gui.addText ("Keep safe")
            nextState = "Safe"
            return (nextState,image)

        if items:
            pt = items[0]
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
            pt = (pt[0]+bbox[0],pt[1]+bbox[1])
            self.gui.addText ("Forsaken Rally Point in " + str(pt[0]) + "," + str(pt[1]))

            # Warping Sequence
            self.rightClick(pt)
            time.sleep (1)
            offset=self.settings["warpToAnomOffset"]
            self.leftClick((pt[0]+offset[0],pt[1]+offset[1]))
            time.sleep (1)
            # Ignoring anom
            self.rightClick(pt)
            time.sleep (1)
            offset=self.settings["ignoreAnomOffset"]
            self.leftClick((pt[0]+offset[0],pt[1]+offset[1]))
            time.sleep (1)

            self.gui.addText ("Waiting 12sec before checking the overview")
            time.sleep(12)

            nextState = "Warping to anom"
        else:
            self.gui.addText ("No Forsaken Rally Point, staying in Init state")
            nextState = "Init"

        image = Image.fromarray(cvImage)
        return (nextState,image)

    def checkAnomHandler(self):
        self.gui.addText("* Check anom state")
        # Cropping the probe scanner
        image=ImageGrab.grab(bbox=self.settings["probeBBox"])
        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.forsaken_rally_point_template)
        if items:
            nextState = "Init"
        else:
            nextState = "Warp off"

        image = Image.fromarray(cvImage)
        return (nextState,image)

    def warpingToAnomHandler(self):
        self.gui.addText("* Warping to anom state")
        #Cropping the overview
        image=ImageGrab.grab(bbox=self.settings["overviewBBox"])

        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.core_template)

        if items:
            self.gui.addText (str(len(items)/2) + " rat(s) found, checking if anom is occupied")

            (res2,items2) = vision.findTemplate(cvImage,self.mobile_tractor_template)

            
            if (vision.isColorPresent(cvImage,(12,31,89),10) == True):
                self.gui.addText ("Anom occupied, starting again in 12sec")

                time.sleep(12) 
                nextState = "Check anom"
            elif (items2):
                self.gui.addText ("MTU found, starting again in 12sec")

                time.sleep(12) 
                nextState = "Check anom"
            else:
                self.gui.addText ("Anom seems free, check again")

                time.sleep(1)
                image=ImageGrab.grab(bbox=self.settings["overviewBBox"])
                cvImage = np.array(image)

                if (vision.isColorPresent(cvImage,(12,31,89),10) == True):
                    self.gui.addText ("Anom occupied, starting again in 10sec")

                    time.sleep(10) 
                    nextState = "Check anom"
                else:
                    self.gui.addText ("Anom free, sleeping 10sec then launch drones")
                    time.sleep(10) 
                    nextState = "Launch drones"
        else:
            self.gui.addText ("No rat yet, staying in Warping to anom state")
            nextState = "Warping to anom"

        image = Image.fromarray(cvImage)
        return (nextState,image)

    def launchDronesHandler(self):
        self.gui.addText("* Launch drones state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=self.settings["dronesBBox"])

        if self.checkLocal():
            self.gui.addText ("Time to safe up")
            nextState = "Align"
            return (nextState,image)

        self.rightClick(self.settings["dronesInBayCoord"])
        time.sleep(1)
        self.leftClick(self.settings["launchDronesCoord"])
        time.sleep(2)

        self.leftClick(self.settings["wreckTabCoord"]) # click wreck tab
        nextState = "Wait wreck"

        return (nextState,image)

    def waitWreckHandler(self):
        self.gui.addText("* Wait wreck state")
        time.sleep(1)
        #Cropping the overview
        bbox=self.settings["overviewBBox"]
        image=ImageGrab.grab(bbox=bbox)

        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.core_template)

        if self.checkLocal():
            self.gui.addText ("Time to safe up")

            self.leftClick(self.settings["mainTabCoord"]) # click main tab
            time.sleep(1)

            nextState = "Align"
            return (nextState,image)

        if items:
            pt = items[0]
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
            pt = (pt[0]+bbox[0],pt[1]+bbox[1])
            self.gui.addText ("Wreck found in (" + str(pt[0]) + "," + str(pt[1]) + ")")
            self.leftClick(pt) # click the wreck
            time.sleep(2)
            self.leftClick(self.settings["orbitCoord"]) # click orbit
            time.sleep(1)
            self.leftClick(self.settings["mainTabCoord"]) # click main tab
            time.sleep(1)

            nextState = "Farming"
        else:
            self.gui.addText ("No wreck yet, staying in Wait wreck state")
            time.sleep(1)
            nextState = "Wait wreck"

        image = Image.fromarray(cvImage)

        return (nextState,image)

    def farmingHandler(self):
        self.gui.addText("* Farming state")

        
        #Cropping the overview
        image=ImageGrab.grab(bbox=self.settings["overviewBBox"])

        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.core_template)

        if self.checkLocal():
            self.gui.addText ("Time to safe up")
            nextState = "Align"
            return (nextState,image)

        if items:
            self.gui.addText (str(len(items)/2) + " rat(s) found, keep farming!")

            time.sleep(1)
            nextState = "Farming"
        else:
            self.gui.addText ("No rat anymore, check again in 5sec")
            time.sleep(5)
            image=ImageGrab.grab(bbox=self.settings["overviewBBox"])
            cvImage = np.array(image)
            (res,items) = vision.findTemplate(cvImage,self.core_template)

            if items:
                self.gui.addText ("False alarm")
                nextState = "Farming"
            else:
                self.gui.addText ("No rat anymore, scoop drones")
                self.anomCounter += 1
                nextState = "Scoop drones"

        image = Image.fromarray(cvImage)
        return (nextState,image)

    def scoopDronesHandler(self):
        self.gui.addText("* Scoop drones state")

        #Cropping the drones window
        image=ImageGrab.grab(bbox=self.settings["dronesBBox"])
        self.rightClick(self.settings["dronesInSpaceCoord"])
        time.sleep(1)
        self.leftClick(self.settings["scoopDronesCoord"])

        self.gui.addText("Waiting 30sec")
        time.sleep(30)

        nextState = "Init"

        return (nextState,image)

    def alignHandler(self):
        self.gui.addText("* Align state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=self.settings["dronesBBox"])
        self.rightClick(self.settings["dronesInSpaceCoord"])
        time.sleep(1)
        self.leftClick(self.settings["scoopDronesCoord"])

        self.rightClick(self.settings["rightClickInSpaceCoord"])
        time.sleep(0.5)
        self.move(self.settings["safeCoord"])
        time.sleep(0.5)
        self.leftClick(self.settings["alignSafeCoord"])

        time.sleep(1)

        self.gui.addText("Waiting 20sec")
        time.sleep(20)

        nextState = "Warp off"
        return (nextState,image)

    def warpOffHandler(self):
        self.gui.addText("* Warp off state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=self.settings["dronesBBox"])

        self.rightClick(self.settings["rightClickInSpaceCoord"])
        time.sleep(0.5)
        self.move(self.settings["safeCoord"])
        time.sleep(0.5)
        self.leftClick(self.settings["warpSafeCoord"])

        #Cancel ignored anoms
        self.move(self.settings["ignoredCoord"])
        time.sleep(2)
        self.leftClick(self.settings["clearAllIgnoredCoord"])

        self.gui.addText ("Wait 1min")
        time.sleep(60)
        nextState = "Safe"
        return (nextState,image)

    def safeHandler(self):
        self.gui.addText("* Safe state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=self.settings["dronesBBox"])

        if self.checkLocal():
            self.gui.addText ("Keep safe")
            time.sleep(1)
            nextState = "Safe"
        else:
            self.gui.addText ("Waiting 60 seconds")
            time.sleep(60)
            nextState = "Init"

        return (nextState,image)
