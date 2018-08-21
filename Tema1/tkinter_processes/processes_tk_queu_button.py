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
   
    root = Tk()
    root.title("Una ventana para Procesos")
    root.resizable(0, 0)
    
    frame = Frame(root)
    frame.pack()

    canvas = Canvas(frame, width=500, height=200, bg="green")
    canvas.pack()
    
    obj = []
    obj.append(canvas.create_oval(10, 10, 20, 20,fill="red"))
    obj.append(canvas.create_oval(30, 10, 40, 20,fill="blue"))
    obj.append(canvas.create_oval(70, 10, 80, 20,fill="black"))


    queue = Queue()

    def ejec_start(): 
        procesos = []
        for x in range(len(obj)):
            procesos.append(Process(target=f, args=(queue,x)))

        for p in procesos:
            p.start()
    
    start = Button(frame, text="Start", command=ejec_start)
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
