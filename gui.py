import Tkinter as tk
import pymouse as pm

import Image, ImageTk

from ast import literal_eval

import gladosEngine as gle

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("GladOS")

        self.mouse = pm.PyMouse()

        # Eve screen capture
        self.screenFrame = tk.Frame()
        self.screenFrame.pack()

        self.screenLabel = tk.Label(self.screenFrame,text="Screen")
        self.screenLabel.pack(in_=self.screenFrame, side=tk.LEFT)

        self.screenStartPositionVar = tk.StringVar()
        self.screenStartPositionEntry = tk.Entry(self.screenFrame, textvariable=self.screenStartPositionVar, width=9)
        self.screenStartPositionEntry.pack(in_=self.screenFrame, side=tk.LEFT)
        self.screenEndPositionVar = tk.StringVar()
        self.screenEndPositionEntry = tk.Entry(self.screenFrame, textvariable=self.screenEndPositionVar, width=9)
        self.screenEndPositionEntry.pack(in_=self.screenFrame, side=tk.LEFT)

        with open("settings.txt") as f: 
            for line in f:
                if "screen" in line:
                    args=line.split()
#                    print args[1]
#                    print args[2]
                    self.screenStartPositionEntry.insert(0,args[1])
                    self.screenEndPositionEntry.insert(0,args[2])

        self.screenWindowOpen = False

        self.screenDisplayButton = tk.Button(self.screenFrame, text="Display", command=self.imageFrame)
        self.screenDisplayButton.pack(in_=self.screenFrame, side=tk.LEFT)

        # Mouse position
        self.mousePositionVar = tk.StringVar()
        self.mousePositionLabel = tk.Label(self,textvariable=self.mousePositionVar)
        self.mousePositionLabel.pack()

        # Catching application close
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

#        self.threadDisplay = threading.Thread(target=self.display)
        startPos = literal_eval(self.screenStartPositionEntry.get())
        endPos = literal_eval(self.screenEndPositionEntry.get())
        self.gladosEngine = gle.GladosEngine(startPos,endPos)
        self.gladosEngine.start()

        self.update()
        self.displayCb()

    def update(self):
        #TODO Move m.position
        self.mousePositionVar.set("Cursor position: {}".format(self.mouse.position()))
        self.after(10,self.update)

    def imageFrame(self):
        # create child window
        if (self.screenWindowOpen == False):
            self.screenWindow = ScreenWindow(self, title="Screen")
            self.screenWindowOpen = True
            self.screenDisplayButton.config(text="Close")
        else:
            self.screenWindow.destroy()
            self.screenWindowOpen = False
            self.screenDisplayButton.config(text="Display")

    def displayCb(self):
        # Call the function in 1sec
        self.after(1000, self.displayCb)

        if self.screenWindowOpen:
            self.screenWindow.update(self.gladosEngine.pilImage)

    def saveScreenSettings(self):
        s = "screen "
        s += self.screenStartPositionEntry.get()
        s += " "
        s += self.screenEndPositionEntry.get()
        s += "\n"
        return s

    def onClosing(self):
#        print("Closing MainFrame")
        with open("settings.txt","w") as f: 
            f.write(self.saveScreenSettings())

        self.gladosEngine.stop()

        self.destroy()

class ScreenWindow(tk.Toplevel):
    def __init__(self,root,title="ScreenWindow"):
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
#        print("Updating ScreenWindow")
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
#        print("Closing ScreenWindow")
        self.root.screenWindowOpen=False
        self.root.screenDisplayButton.config(text="Display")
        self.destroy()
