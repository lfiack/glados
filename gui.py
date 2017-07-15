import Tkinter as tk
import Image, ImageTk

#TODO move
import pymouse as pm
import pykeyboard as pk

from ast import literal_eval

from random import randint

import time
import evestate
#import logreader

class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("GladOS")

        self.mouse = pm.PyMouse()

        self.evestate = evestate.EveState()

        self.hitDscanVar = tk.IntVar()

        # Overview
        self.overviewWindowLine = EveWindowLine(self,"Overview")
        startPos=literal_eval(self.overviewWindowLine.startPositionEntry.get())
        endPos=literal_eval(self.overviewWindowLine.endPositionEntry.get())
        self.evestate.addEveWindow(evestate.EveWindow("Overview",startPos,endPos))
        # Dscan
        self.dscanWindowLine = EveWindowLine(self,"Dscan")
        startPos=literal_eval(self.dscanWindowLine.startPositionEntry.get())
        endPos=literal_eval(self.dscanWindowLine.endPositionEntry.get())
        self.evestate.addEveWindow(evestate.EveWindow("Dscan",startPos,endPos))
        # Probe
        self.probeWindowLine = EveWindowLine(self,"Probe")
        startPos=literal_eval(self.probeWindowLine.startPositionEntry.get())
        endPos=literal_eval(self.probeWindowLine.endPositionEntry.get())
        self.evestate.addEveWindow(evestate.EveWindow("Probe",startPos,endPos))
        # Item
        self.itemWindowLine = EveWindowLine(self,"Item")
        startPos=literal_eval(self.itemWindowLine.startPositionEntry.get())
        endPos=literal_eval(self.itemWindowLine.endPositionEntry.get())
        self.evestate.addEveWindow(evestate.EveWindow("Item",startPos,endPos))

        self.readEveClientCb()

        # Hit Dscan
        self.hitDscanCheckbutton = tk.Checkbutton(self, text="Hit Dscan", command=self.hitDscanCb, variable = self.hitDscanVar)
        self.hitDscanCheckbutton.pack()

        # Mouse position
        self.mousePositionVar = tk.StringVar()
        self.mousePositionLabel = tk.Label(self,textvariable=self.mousePositionVar)
        self.mousePositionLabel.pack()

        # Keyboard
        self.k = pk.PyKeyboard()

        # Catching application close
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.update()

    def update(self):
        #TODO Move m.position
        self.mousePositionVar.set("Cursor position: {}".format(self.mouse.position()))
        self.after(10,self.update)

    # That's the main loop
    def readEveClientCb(self):
        # Call the function in 1sec
        self.after(1000, self.readEveClientCb)

        print "====================="
        print "New Step"
        print "====================="
#        print("Taking screens")
        start = time.time()

        self.evestate.compute()

        for w in self.evestate.eveWindowList:
            if w.name == "Overview":
                self.displayScreen(self.overviewWindowLine, w.pilImage)
            elif w.name == "Dscan":
                self.displayScreen(self.dscanWindowLine, w.pilImage)
            elif w.name == "Probe":
                self.displayScreen(self.probeWindowLine, w.pilImage)
            elif w.name == "Item":
                self.displayScreen(self.itemWindowLine, w.pilImage)

        end = time.time()
        print(end - start)

        self.evestate.display()

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
            f.write(self.itemWindowLine.saveSettings())
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
        self.endPositionVar = tk.StringVar()
        self.endPositionEntry = tk.Entry(self.frame, textvariable=self.endPositionVar, width=9)
        self.endPositionEntry.pack(in_=self.frame, side=tk.LEFT)

        with open("settings.txt") as f: 
            for line in f:
                if self.title in line:
                    args=line.split()
#                    print args[1]
#                    print args[2]
                    self.startPositionEntry.insert(0,args[1])
                    self.endPositionEntry.insert(0,args[2])


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
        s += self.endPositionEntry.get()
        s += "\n"
        return s
