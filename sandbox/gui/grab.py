#!/usr/bin/python
import pyscreenshot as ImageGrab

from Tkinter import *
import Image, ImageTk
import time

class MainWindow():

    #----------------

    def __init__(self, main):

        # canvas for image
        self.canvas = Canvas(main, width=500, height=500)
        self.canvas.grid(row=0, column=0)

        self.pilImage = ImageGrab.grab(bbox=(0,0,500,500))
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.sprite = self.canvas.create_image(0,0,image=self.image,anchor=NW)

        self.update()

    def update(self):
        print("a")
        self.pilImage=ImageGrab.grab(bbox=(0,0,500,500))
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.canvas.itemconfig(self.sprite, image = self.image)
        root.after(1000, self.update)
    


root = Tk()
MainWindow(root)
root.mainloop()
