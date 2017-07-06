import Tkinter as tk
import Image, ImageTk

#TODO move
import pymouse as pm
import pyscreenshot as ImageGrab


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
        self.dscanStartPositionEntry.pack(in_=self.dscanFrame, side=tk.LEFT)
        self.dscanStopPositionVar = tk.StringVar()
        self.dscanStopPositionEntry = tk.Entry(self.dscanFrame, textvariable=self.dscanStopPositionVar, width=9)
        self.dscanStopPositionEntry.pack(in_=self.dscanFrame, side=tk.LEFT)

        self.dscanDisplayButton = tk.Button(self.dscanFrame, text="Display", command=self.imageFrame)
#        self.dscanDisplayButton = tk.Button(self.dscanFrame, text="Display", command=self.quit)
        self.dscanDisplayButton.pack(in_=self.dscanFrame, side=tk.LEFT)

        # Mouse position
        self.mousePositionVar = tk.StringVar()
        self.mousePositionLabel = tk.Label(self,textvariable=self.mousePositionVar)
        self.mousePositionLabel.pack()

#        self.canvas = tk.Canvas(self)
#        self.canvas.pack()
#        self.im=ImageGrab.grab(bbox=(10,10,500,500))
#        self.image = ImageTk.PhotoImage(self.im)
#        self.imagesprite = self.canvas.create_image(500,500,image=self.image)

        self.update()

    def update(self):
        #TODO Move m.position
        self.mousePositionVar.set("Cursor position: {}".format(self.mouse.position()))
        self.after(10,self.update)

    def imageFrame(self):
        # create child window
        self.win = tk.Toplevel()
        self.win.title("Toto")
        self.canvas = tk.Canvas(self.win, width=500, height=500)
        self.canvas.grid(row=0, column=0)

        self.pilImage = ImageGrab.grab(bbox=(0,0,500,500))
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.sprite = self.canvas.create_image(0,0,image=self.image,anchor=tk.NW)

        self.updateImageFrame()

    def updateImageFrame(self):
        print("a")
        self.pilImage=ImageGrab.grab(bbox=(0,0,500,500))
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas.itemconfig(self.sprite, image = self.image)
        self.after(1000, self.updateImageFrame)
