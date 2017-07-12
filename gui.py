import Tkinter as tk
import Image, ImageTk

#TODO move
import pymouse as pm
import pyscreenshot as ImageGrab

from ast import literal_eval

class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("GladOS")

        self.mouse = pm.PyMouse()

        # Dscan
        self.dscanFrame = tk.Frame()
        self.dscanFrame.pack()

        self.dscanLabel = tk.Label(self.dscanFrame,text="Dscan")
        self.dscanLabel.pack(in_=self.dscanFrame, side=tk.LEFT)

        self.dscanStartPositionVar = tk.StringVar()
        self.dscanStartPositionEntry = tk.Entry(self.dscanFrame, textvariable=self.dscanStartPositionVar, width=9)
        self.dscanStartPositionEntry.insert(0,"0,0")
        self.dscanStartPositionEntry.pack(in_=self.dscanFrame, side=tk.LEFT)
        self.dscanStopPositionVar = tk.StringVar()
        self.dscanStopPositionEntry = tk.Entry(self.dscanFrame, textvariable=self.dscanStopPositionVar, width=9)
        self.dscanStopPositionEntry.insert(0,"500,500")
        self.dscanStopPositionEntry.pack(in_=self.dscanFrame, side=tk.LEFT)

        self.dscanDisplayButton = tk.Button(self.dscanFrame, text="Display", command=self.imageFrame)
#        self.dscanDisplayButton = tk.Button(self.dscanFrame, text="Display", command=self.quit)
        self.dscanDisplayButton.pack(in_=self.dscanFrame, side=tk.LEFT)

        # Mouse position
        self.mousePositionVar = tk.StringVar()
        self.mousePositionLabel = tk.Label(self,textvariable=self.mousePositionVar)
        self.mousePositionLabel.pack()

        self.winOpen = 0
        self.screenshot()

        self.update()

    def update(self):
        #TODO Move m.position
        self.mousePositionVar.set("Cursor position: {}".format(self.mouse.position()))
        self.after(10,self.update)

    def imageFrame(self):
        # create child window
        self.win = SubFrame(self)
        self.winOpen = 1

    def screenshot(self):
        print("Taking screenshot")
        posStart=literal_eval(self.dscanStartPositionEntry.get())
        posStop=literal_eval(self.dscanStopPositionEntry.get())
        print(str(posStart))
        print(str(posStop))
        self.pilImage=ImageGrab.grab(bbox=(posStart[0],posStart[1],posStop[0],posStop[0]))
        if (self.winOpen):
            self.win.update(self.pilImage)
        self.after(1000, self.screenshot)

class SubFrame(tk.Toplevel):
    def __init__(self,root):
        tk.Toplevel.__init__(self)
        self.root=root
        self.title("SubFrame")
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0)
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def update(self,pilImage):
        print("Updating SubFrame")
        self.image = ImageTk.PhotoImage(pilImage)
        self.sprite = self.canvas.create_image(0,0,image=self.image,anchor=tk.NW)
        self.canvas.itemconfig(self.sprite, image = self.image)

    def onClosing(self):
        print("Closing SubFrame")
        self.root.winOpen=0
        self.destroy()
