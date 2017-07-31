import Image, ImageTk
import pyscreenshot as ImageGrab

import cv2  
import numpy as np

from pymouse import PyMouse

import threading
import time

import fsm
import vision

class GladosEngine(threading.Thread):
    def __init__(self,startPos,endPos):
        threading.Thread.__init__(self)
        self.startPos = startPos
        self.endPos = endPos
        self.pilImage=Image

        self.mouse = PyMouse()

        self.fsm = fsm.StateMachine()

        self.forsaken_rally_point_template = cv2.imread("./data/Forsaken_Rally_Point.png")
        self.core_template = cv2.imread("./data/Core.png")
        self.allied_template = cv2.imread("./data/Allied.png")
        self.neutral_template = cv2.imread("./data/Neutral.png")
        self.hostile_template = cv2.imread("./data/Red.png")

        self.fsm.addState("Init", self.startHandler)
        self.fsm.addState("Warping to anom", self.warpingToAnomHandler)
        self.fsm.addState("Launch drones", self.launchDronesHandler)
        self.fsm.addState("Wait wreck", self.waitWreckHandler)
        self.fsm.addState("Farming", self.farmingHandler)
        self.fsm.addState("Scoop drones", self.scoopDronesHandler)

        self.fsm.addState("Align", self.alignHandler)
        self.fsm.addState("Warp off", self.warpOffHandler)
        self.fsm.addState("Safe", self.safeHandler)
        self.fsm.addState("Wait", self.waitHandler)

        self.fsm.setStart("Farming")
#        self.fsm.setStart("Init")

        self.running = True

    def rightClick(self,coordinates):
        print "Right click in " + str(coordinates[0]) + "," + str(coordinates[1])
        self.mouse.move(coordinates[0],coordinates[1])
        time.sleep(0.1)
        self.mouse.press(coordinates[0],coordinates[1],button=2)
        time.sleep(0.15)
        self.mouse.release(coordinates[0],coordinates[1],button=2)
        time.sleep(0.5)

    def leftClick(self,coordinates):
        print "Left click in " + str(coordinates[0]) + "," + str(coordinates[1])
        self.mouse.move(coordinates[0],coordinates[1])
        time.sleep(0.1)
        self.mouse.press(coordinates[0],coordinates[1],button=1)
        time.sleep(0.15)
        self.mouse.release(coordinates[0],coordinates[1],button=1)
        time.sleep(0.5)

    def checkLocal(self):
        image=ImageGrab.grab(bbox=(1785,65,1919,1199))
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

        (res,items) = vision.findTemplate(cvImage,self.hostile_template)
        if items:
            hostile = len(items)
        else:
            hostile = 0

        return (allied, neutral, hostile)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            print ("=====================")
            print (time.strftime("%d/%m/%Y - %H:%M:%S"))
            self.pilImage=self.fsm.step()

            time.sleep(0.2)

    def startHandler(self):
        print("* Init state")
        # Cropping the probe scanner
        image=ImageGrab.grab(bbox=(1410,115,1785,1199))
        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.forsaken_rally_point_template)
        if items:
            pt = items[0]
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
            pt = (pt[0]+1410,pt[1]+115)
            print ("Forsaken Rally Point in " + str(pt[0]) + "," + str(pt[1]))

            # Warping Sequence
            self.rightClick(pt)
            time.sleep (1)
            self.leftClick((pt[0]+25,pt[1]+10))
            time.sleep (1)
            # Ignoring anom
            self.rightClick(pt)
            time.sleep (1)
            self.leftClick((pt[0]+25,pt[1]+75))
            time.sleep (1)

            nextState = "Warping to anom"
        else:
            print "No Forsaken Rally Point, staying in Init state"
            nextState = "Init"

        image = Image.fromarray(cvImage)
        return (nextState,image)

    def warpingToAnomHandler(self):
        print("* Warping to anom state")
        #Cropping the overview
        image=ImageGrab.grab(bbox=(90,460,490,880))

        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.core_template)

        if items:
            print (str(len(items)/2) + " rat(s) found, checking if anom is occupied")

            if (vision.isColorPresent(cvImage,(12,31,89),10) == True):
                print ("Anom occupied, starting again in 12sec")

                time.sleep(12) 
                nextState = "Init"
            else:
                print ("Anom free, sleeping 12sec then launch drones")

                time.sleep(12) 
                nextState = "Launch drones"
        else:
            print ("No rat yet, staying in Warping to anom state")
            nextState = "Warping to anom"

        image = Image.fromarray(cvImage)
        return (nextState,image)

    def launchDronesHandler(self):
        print("* Launch drones state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=(95,880,490,1199))
        self.rightClick((140,920))
        time.sleep(1)
        self.leftClick((165,925))
        time.sleep(2)

        nextState = "Wait wreck"

        return (nextState,image)

    def waitWreckHandler(self):
        print("* Wait wreck state")
        self.leftClick((300,435)) # click wreck tab
        time.sleep(1)
        #Cropping the overview
        image=ImageGrab.grab(bbox=(90,460,490,880))

        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.core_template)

        if items:
            pt = items[0]
            cv2.rectangle(cvImage, pt, (pt[0] + 2, pt[1] + 2), (255, 0, 0), 2)
            pt = (pt[0]+90,pt[1]+460)
            print "Wreck found in (" + str(pt[0]) + "," + str(pt[1]) + ")"
            self.leftClick(pt) # click the wreck
            time.sleep(2)
            self.leftClick((210,375)) # click orbit
            time.sleep(1)
            self.leftClick((175,435)) # click main tab
            time.sleep(1)

            nextState = "Farming"
        else:
            print ("No wreck yet, staying in Wait wreck state")
            nextState = "Wait wreck"

        image = Image.fromarray(cvImage)

        return (nextState,image)

    def farmingHandler(self):
        print("* Farming state")

        
        #Cropping the overview
        image=ImageGrab.grab(bbox=(90,460,490,880))

        cvImage = np.array(image)
        (res,items) = vision.findTemplate(cvImage,self.core_template)

        (allied,neutral,hostile)=self.checkLocal()
        print str(allied) + " allies, " + str(neutral) + " neutrals, " + str(hostile) + " hostiles"
        if neutral or hostile:
            print ("Time to safe up")
            nextState = "Align"
            return (nextState,image)

        if items:
            print (str(len(items)/2) + " rat(s) found, keep farming!")

            time.sleep(1)
            nextState = "Farming"
        else:
            print ("No rat anymore, check again in 5sec")
            time.sleep(5)
            image=ImageGrab.grab(bbox=(90,460,490,880))
            cvImage = np.array(image)
            (res,items) = vision.findTemplate(cvImage,self.core_template)

            if items:
                print ("False alarm")
                nextState = "Farming"
            else:
                print ("No rat anymore, scoop drones")
                nextState = "Scoop drones"

        image = Image.fromarray(cvImage)
        return (nextState,image)

    def scoopDronesHandler(self):
        print("* Scoop drones state")

        #Cropping the drones window
        image=ImageGrab.grab(bbox=(95,880,490,1199))
        self.rightClick((140,960))
        time.sleep(1)
        self.leftClick((165,1005))

        print("Waiting 30sec")
        time.sleep(30)

        nextState = "Init"

        return (nextState,image)

    def alignHandler(self):
        print("* Align state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=(95,880,490,1199))
        self.rightClick((140,960))
        time.sleep(1)
        self.leftClick((165,1005))

        self.rightClick((500,100))
        time.sleep(0.5)
        self.mouse.move(700,240)
        time.sleep(0.5)
        self.leftClick((800,270))

        print("Waiting 20sec")
        time.sleep(20)

        nextState = "Warp off"
        return (nextState,image)

    def warpOffHandler(self):
        print("* Warp off state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=(95,880,490,1199))

        self.rightClick((500,100))
        time.sleep(0.5)
        self.mouse.move(700,240)
        time.sleep(0.5)
        self.leftClick((800,240))

        print "Wait 2min"
        time.sleep(120)
        nextState = "Safe"
        return (nextState,image)

    def safeHandler(self):
        print("* Safe state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=(95,880,490,1199))

        (allied,neutral,hostile)=self.checkLocal()
        print str(allied) + " allies, " + str(neutral) + " neutrals, " + str(hostile) + " hostiles"
        if neutral or hostile:
            print ("Keep safe")
            nextState = "Safe"
        else:
            nextState = "Wait"

        return (nextState,image)

    def waitHandler(self):
        print("* Wait state")
        #Cropping the drones window
        image=ImageGrab.grab(bbox=(95,880,490,1199))
        time.sleep(600)
        nextState = "Init"
        return (nextState,image)
