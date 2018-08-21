# -*- coding: utf-8 -*-
from Tkinter import Tk, Frame, Canvas, Label, Button, Entry, END 
import time, random

if __name__ == '__main__':     
    window = Tk()
    window.title("Una ventana de prueba")    
    
    frame = Frame(window)
    frame.pack()

    canvas = Canvas(frame, width=500, height=200, bg="green") 
    id1 = canvas.create_oval(50, 20, 70, 40, fill="white")
    id2 = canvas.create_rectangle(100,100,125,125, fill ="red")
    canvas.pack()
        
    def click(event): 
        print "raton en", event.x, event.y       
        colors = ["green","yellow","red", "black", "white"]     
        canvas.itemconfigure(id2,fill=colors[random.randint(0,len(colors)-1)])
        o = canvas.coords(id1)
        print "origin", o, type(o)
        r = o[0:2]+map(lambda x: x+4,o[-2:])
        print "result", r, type(r)
        canvas.coords(id1,r[0],r[1],r[2],r[3])
    canvas.bind("<Button-1>", click)        
   
    def ejecucion_boton():
        print "boton"        
        canvas.move(id1,10,10)       
        l.configure(text="pero...ha cambiado!"+str(random.random()))
        entrada.delete(0,END)
        entrada.insert(0,"hola"+str(time.gmtime()[5]))

    boton = Button(frame, text="texto de botón", command=ejecucion_boton)
    boton.pack()

    l = Label(frame, text="Un texto de etiqueta")
    l.pack()

    entrada = Entry(frame,width=25)
    entrada.pack()

    window.mainloop()
