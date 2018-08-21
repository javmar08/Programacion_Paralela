# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Canvas, Label
import time, random

if __name__ == '__main__':    
 
    window = Tk()
    window.title("Una ventana de prueba")    
    
    frame = Frame(window)
    frame.pack()

    canvas = Canvas(frame, width=800, height=500) 
    canvas.create_oval(50, 20, 100, 70, fill="white")
    canvas.create_rectangle(100, 100, 150, 150, fill ="red")
    canvas.pack()
    
    l = Label(frame, text="Un texto de etiqueta")
    l.pack()

    window.mainloop()
