from multiprocessing import Process
from multiprocessing import Queue

from Tkinter import *
import time, random

def f(q,i):
    for x in range(10):
        print "process", i, "ejecutando", x 
        time.sleep(random.random())
        q.put((i,random.randint(5,25),random.randint(5,10)))

    print "termina proceso"


if __name__ == '__main__':    

    queue = Queue()

    root = Tk()
    root.title("Una ventana para Procesos")
    root.resizable(0, 0)
    
    def move(event):        
        print "raton moviendose", event.x, event.y
    
    frame = Frame(root)    
    frame.pack()

    canvas = Canvas(frame, width=500, height=200, bg="green")
    canvas.pack()

    def click(event): 
        print "raton en", event.x, event.y       
    canvas.bind("<Button-1>", click)  
    
    def move(event):        
        print "raton moviendose", event.x, event.y
    canvas.bind("<Motion>", move)

    obj = []
    obj.append(canvas.create_oval(10, 10, 20, 20,fill="red"))
    obj.append(canvas.create_oval(30, 10, 40, 20,fill="blue"))

    print obj
  
    def ejec_star(): 
        p = Process(target=f, args=(queue,0))#0 es el circulo rojo
        q = Process(target=f, args=(queue,1))#1 es el circulo azul

        p.start()
        q.start()
    
    start = Button(frame, text="Start", command=ejec_star)
    start.pack()

    def ejec_end():
        queue.put("quit")

    end = Button(frame, text="End", command=ejec_end)
    end.pack()

    try:
        while 1:
            if not queue.empty():
                s = queue.get()
                if s  == 'quit':
                    break
                else:
                    canvas.move(obj[s[0]],s[1],s[2])            
            root.update() 
    except TclError:
        pass
