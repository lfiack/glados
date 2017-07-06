#!/usr/bin/python
# coding: utf-8

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here

from pymouse import PyMouse

m = PyMouse()

def update():
    strl.set("mouse at {0}".format(m.position()))
    root.after(10, update)

root = Tk()
strl = StringVar()
lab = Label(root,textvariable=strl)
lab.pack()
update()
root.title("Mouseposition")
root.mainloop()
