from multiprocessing import Process
from multiprocessing import Queue

from Tkinter import *
import time, random

def f(q,i):
    for x in range(10):
        print "process", i, "ejecutando", x 
        time.sleep(random.random())
        q.put((i,4,4))
    q.put("quit");
    print "termina proceso"

if __name__ == '__main__':    
    root = Tk()
    root.title("Una ventana para Procesos")
    root.resizable(0, 0)

    frame = Frame(root)
    frame.pack()

    canvas = Canvas(frame, width=500, height=200)
    canvas.pack()

    obj = []
    obj.append(canvas.create_oval(10, 10, 20, 20,fill="red"))
    obj.append(canvas.create_oval(30, 10, 40, 20,fill="blue"))

    queue = Queue()

    p = Process(target=f, args=(queue,0))
    q = Process(target=f, args=(queue,1))
    
    p.start()
    q.start()

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
