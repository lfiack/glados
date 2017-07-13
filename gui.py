import Tkinter as tk
import Image, ImageTk

#TODO move
import pymouse as pm
import pykeyboard as pk
import pyscreenshot as ImageGrab

from ast import literal_eval

from random import randint

import time
import probe
import dscan
import overview

class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("GladOS")

        self.mouse = pm.PyMouse()

        self.probe = probe.Probe()
        self.dscan = dscan.Dscan()
        self.overview = overview.Overview()

        self.hitDscanVar = tk.IntVar()

        # Overview
        self.overviewWindowLine = EveWindowLine(self,"Overview")
        # Dscan
        self.dscanWindowLine = EveWindowLine(self,"Dscan")
        # Probe
        self.probeWindowLine = EveWindowLine(self,"Probe")

        self.grabScreenCb()

        # Hit Dscan
        self.hitDscanCheckbutton = tk.Checkbutton(self, text="Hit Dscan", command=self.hitDscanCb, variable = self.hitDscanVar)
        self.hitDscanCheckbutton.pack()

        # Mouse position
        self.mousePositionVar = tk.StringVar()
        self.mousePositionLabel = tk.Label(self,textvariable=self.mousePositionVar)
        self.mousePositionLabel.pack()

        self.k = pk.PyKeyboard()

        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.update()

    def update(self):
        #TODO Move m.position
        self.mousePositionVar.set("Cursor position: {}".format(self.mouse.position()))
        self.after(10,self.update)

    def grabScreenCb(self):
        # Call the function in 1sec
        self.after(1000, self.grabScreenCb)
#        print("Taking screens")
        start = time.time()

        # Grab the entire screen
        self.pilImage=ImageGrab.grab()

        # Crop, compute and display the overview
        pilImage = self.cropScreen(self.overviewWindowLine)
        pilImage = self.overview.compute(pilImage)
        self.displayScreen(self.overviewWindowLine, pilImage)

        # Crop, compute and display the dscan
        pilImage = self.cropScreen(self.dscanWindowLine)
        pilImage = self.dscan.compute(pilImage)
        self.displayScreen(self.dscanWindowLine, pilImage)

        # Crop, compute and display the probe window
        pilImage = self.cropScreen(self.probeWindowLine)
        pilImage = self.probe.compute(pilImage)
        self.displayScreen(self.probeWindowLine, pilImage)

        end = time.time()
        print(end - start)

    def cropScreen(self,eveWindowLine):
        # Read the Coordinates of the screenshot from the corresponding Entry
        posStart=literal_eval(eveWindowLine.startPositionEntry.get())
        posStop=literal_eval(eveWindowLine.stopPositionEntry.get())
#        print(str(posStart))
#        print(str(posStop))
        area = (posStart[0],posStart[1],posStop[0],posStop[1])
        return self.pilImage.crop(area)

    def displayScreen(self,eveWindowLine,pilImage):
        # Update the image in the window if it's open
        if (eveWindowLine.windowOpen):
            eveWindowLine.win.update(pilImage)

    def onClosing(self):
#        print("Closing MainFrame")
        with open("settings.txt","w") as f: 
            f.write(self.overviewWindowLine.saveSettings())
            f.write(self.dscanWindowLine.saveSettings())
            f.write(self.probeWindowLine.saveSettings())
        self.destroy()

    def hitDscanCb(self):
        if self.hitDscanVar.get():
            self.hitDscan()

    def hitDscan(self):
        print("Hitting Dscan")
        self.k.tap_key('v')
        if self.hitDscanVar.get():
            delay=randint(1000, 3000)
            self.after(delay,self.hitDscan)

class SubFrame(tk.Toplevel):
    def __init__(self,root,title="SubFrame"):
        tk.Toplevel.__init__(self)
        self.root=root
        self.resizable(0,0)
        self.width=0
        self.height=0
        self.title(title)
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0)
        self.canvas.pack()
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def update(self,pilImage):
#        print("Updating SubFrame")
        # Convert the image
        self.image = ImageTk.PhotoImage(pilImage)

        # Adapt the size of the canvas
        width, height = pilImage.size
        if (self.width != width or self.height != height):
#            print("Size changed")
            self.width, self.height = width, height
#            print("%dx%d" % (self.width,self.height))
            self.canvas.config(width=self.width, height=self.height)
            self.geometry("%dx%d" % (self.width,self.height))

        # Update the image
        self.sprite = self.canvas.create_image(0,0,image=self.image,anchor=tk.NW)
        self.canvas.itemconfig(self.sprite, image = self.image)

    def onClosing(self):
#        print("Closing SubFrame")
        self.root.windowOpen=0
        self.root.displayButton.config(text="Display")
        self.destroy()

class EveWindowLine:
    def __init__(self,root,title):
#        print("Create EveWindowLine " + title)
        self.root = root
        self.title = title
        self.frame = tk.Frame()
        self.frame.pack()

        self.label = tk.Label(self.frame,text=self.title)
        self.label.pack(in_=self.frame, side=tk.LEFT)

        self.startPositionVar = tk.StringVar()
        self.startPositionEntry = tk.Entry(self.frame, textvariable=self.startPositionVar, width=9)
        self.startPositionEntry.pack(in_=self.frame, side=tk.LEFT)
        self.stopPositionVar = tk.StringVar()
        self.stopPositionEntry = tk.Entry(self.frame, textvariable=self.stopPositionVar, width=9)
        self.stopPositionEntry.pack(in_=self.frame, side=tk.LEFT)

        with open("settings.txt") as f: 
            for line in f:
                if self.title in line:
                    args=line.split()
#                    print args[1]
#                    print args[2]
                    self.startPositionEntry.insert(0,args[1])
                    self.stopPositionEntry.insert(0,args[2])


        self.displayButton = tk.Button(self.frame, text="Display", command=self.imageFrame)
        self.displayButton.pack(in_=self.frame, side=tk.LEFT)

        self.windowOpen = 0

    def imageFrame(self):
        # create child window
        if (self.windowOpen == 0):
            self.win = SubFrame(self, title=self.title)
            self.windowOpen = 1
            self.displayButton.config(text="Close")
        else:
            self.win.destroy()
            self.windowOpen = 0
            self.displayButton.config(text="Display")

    def saveSettings(self):
        s = ""
        s += self.title
        s += " "
        s += self.startPositionEntry.get()
        s += " "
        s += self.stopPositionEntry.get()
        s += "\n"
        return s
