import Tkinter as tk
import pymouse as pm

import Image, ImageTk

from ast import literal_eval

import gladosEngine as gle

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("GladOS")
        self.minsize(400,500)

        self.mouse = pm.PyMouse()

        # Reset state configuration
        self.resetStateFrame = tk.Frame()
        self.resetStateFrame.pack()

        self.resetStateLabel = tk.Label(self.resetStateFrame,text="Reset State")
        self.resetStateLabel.pack(in_=self.resetStateFrame, side=tk.LEFT)

        self.resetStateEntry = tk.Entry(self.resetStateFrame, width=15)
        self.resetStateEntry.insert(0, "Init")
        self.resetStateEntry.pack()

        # Control Buttons
        self.buttonsFrame = tk.Frame()
        self.buttonsFrame.pack()

        self.screenWindowOpen = False
        self.botStarted = False

        self.startButton = tk.Button(self.buttonsFrame, text="Start", command=self.startBot)
        self.startButton.pack(in_=self.buttonsFrame, side=tk.LEFT)

        self.resetButton = tk.Button(self.buttonsFrame, text="Reset", command=self.resetBot)
        self.resetButton.pack(in_=self.buttonsFrame, side=tk.LEFT)

        self.screenDisplayButton = tk.Button(self.buttonsFrame, text="Display", command=self.imageFrame)
        self.screenDisplayButton.pack(in_=self.buttonsFrame, side=tk.LEFT)

        # Engine text
        self.engineText = ""
        self.engineTextVar = tk.StringVar()
        self.engineTextLabel = tk.Label(self,textvariable=self.engineTextVar,justify=tk.LEFT,bg='white',anchor = tk.NW)
        self.engineTextLabel.pack(expand=1,fill=tk.BOTH)

        # Mouse position
        self.mousePositionVar = tk.StringVar()
        self.mousePositionLabel = tk.Label(self,textvariable=self.mousePositionVar)
        self.mousePositionLabel.pack()

        # Catching application close
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

#        self.threadDisplay = threading.Thread(target=self.display)
        self.gladosEngine = gle.GladosEngine(self)
        self.gladosEngine.start()

        self.update()
        self.displayCb()

    def update(self):
        self.mousePositionVar.set("Cursor position: {}".format(self.mouse.position()))
        self.after(10,self.update)

    def resetText(self):
        self.engineText = ""

    def addText(self, text):
        self.engineText += text
        self.engineText += "\n"
        self.engineTextVar.set(self.engineText)

    def setText(self, text):
        self.engineText=text
        self.engineTextVar.set(self.engineText)

    def logText(self):
        print self.engineText   # TODO actual log

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

    def startBot(self):
        if (self.botStarted):
            self.setText("Bot stopped")
            self.botStarted = False
            self.gladosEngine.stopBot()
            self.startButton.config(text="Start")
        else:
            self.setText("Bot started")
            self.botStarted = True
            self.gladosEngine.startBot()
            self.startButton.config(text="Stop")

    def resetBot(self):
        if (self.botStarted):
#            print "Stop bot first"
            self.setText("Stop bot first")
        else:
#            print "Reset bot to " + self.resetStateEntry.get() + " state"
            self.setText("Reset bot to " + self.resetStateEntry.get() + " state")
            self.gladosEngine.resetBot(self.resetStateEntry.get())

    def displayCb(self):
        # Call the function in 1sec
        self.after(1000, self.displayCb)

        if self.screenWindowOpen:
            self.screenWindow.update(self.gladosEngine.pilImage)

#    def saveScreenSettings(self):
#        s = "screen "
#        s += self.screenStartPositionEntry.get()
#        s += " "
#        s += self.screenEndPositionEntry.get()
#        s += "\n"
#        return s

    def onClosing(self):
#        print("Closing MainFrame")
#        with open("settings.txt","w") as f: 
#            f.write(self.saveScreenSettings())

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
