# -*- coding: utf-8 -*-
from Tkinter import *
import time, random

if __name__ == '__main__':    
 
    root = Tk()
    root.title("Una ventana de prueba")    
    
    frame = Frame(root)
    frame.pack()

    canvas = Canvas(frame, width=500, height=200, bg="green") 
    canvas.grid(row=0, column=0)
    id1 = canvas.create_oval(50, 20, 70, 40, fill="white")
    id2 = canvas.create_rectangle(100,100,125,125, fill ="red")
   
    def click(event): 
        colors = ["green","yellow","red", "black", "white"]
        print "raton en", event.x, event.y       
        canvas.itemconfigure(id2,fill=colors[random.randint(0,len(colors)-1)])
      
    canvas.bind("<Button-1>", click)        
   
    def ejecucion_boton():
        print "boton"        
        canvas.move(id1,10,10)        
        l.configure(text="pero...ha cambiado!"+str(random.random()))

    boton = Button(frame, text="texto de boton", command=ejecucion_boton)
    boton.grid(row=1,column=0)
   
    l = Label(frame, text="Un texto de etiqueta")
    l.grid(row=0,column=1)
   
    entrada = Entry(frame,width=25)
    entrada.grid(row=1,column=1)
  
    root.mainloop()
