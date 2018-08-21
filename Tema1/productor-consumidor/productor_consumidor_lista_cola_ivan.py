# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:02:09 2015

@author: alumno
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 16:13:17 2015

@author: javier
"""

from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import BoundedSemaphore
from time            import sleep
from random          import random
from multiprocessing import Manager
from multiprocessing import Queue
from Tkinter         import *

'''
Vamos ahora a generalizar este proceso, añadiendo un
almacén más grande. Para ello vamos a observar un par
de cosas

* Vamos a utiliar BoundedSemaphore, que es similar
al lock, pero para cerrarse tiene que cerrarse N veces
consecutivas, y lo mismo para abrirse.

* Por otra parte necesitamos tratar con más detalle 
la memoria compartida por ambos procesos. Aquí hay dos
opciones. Trabajar con las estructuras de de datos
dadas por multiprocessing (Value, Array, Queue), que 
son más eficientes, o usar un Manager para utilizar las
estructuras de Python de toda la vida, aunque esto será
menos eficiente.
'''

'''
Vamos a hacerlo ahora usando Manager
'''
ALMACEN = ''
N = 10
K = 3

def tardar():
    sleep(random()/3)

def producir(almacen, puertaDejar, puertaRecoger, cambios):
    for value in range(N):
        #print current_process().name, 'produciendo',
        tardar()
        cambios.put((0, 'yellow', None))
        puertaDejar.acquire() #se va a la puerta a esperar, y cuando pasa la cierra
        almacen.append(value)
        cambios.put((0, 'light blue', str(value)+' '))
        puertaRecoger.release() #cuando acaba, abre la otra
        print current_process().name, 'almacenado', value


def consumir(almacen, puertaDejar, puertaRecoger, cambios):
    for value in range(N):
        puertaRecoger.acquire() #se va a la puerta a esperar, y cuando le toca, la cierra
        # Siempre que vamos a una puerta puede estar
        # abierta o cerrada. Si está abierta pasamos
        # si está cerrada esperamos.
        dato = almacen.pop(0)
        print current_process().name, 'desalmacenando', dato
        cambios.put((1, 'yellow', 'quitar'))
        puertaDejar.release()
        #print current_process().name, 'consumiento', dato
        tardar()
        cambios.put((1, 'light blue', None))

if __name__ == '__main__':
    
    root = Tk()
    root.title("Una ventana para Procesos")
    root.resizable(0, 0)
    
    frame = Frame(root)
    frame.pack()

    canvas = Canvas(frame, width=600, height=300, bg="light green")
    canvas.pack()
    
    obj = []
    obj.append(canvas.create_oval( 30, 100, 130, 200,fill="light blue"))
    obj.append(canvas.create_oval(470, 100, 570, 200,fill="light blue"))
    
    textProd = canvas.create_text( 80, 150, text = 'Productor')
    textCons = canvas.create_text(520, 150, text = 'Consumidor')

    root.update()
    
    cambios = Queue()
    manager = Manager()
    almacen = manager.list()
    
    textAlmacen = canvas.create_text(300, 150, text = '')
        
    print 'Almacén inicial : ', almacen[:]
    
    puertaDejar   = BoundedSemaphore(K) #almacén de tamaño 3
    puertaRecoger = BoundedSemaphore(K)
    
    for i in range(K):
        puertaRecoger.acquire()

    #Las puertas se crean abiertas. Esta hay que cerrarla
    #al inicio.
    
    def start():
        productor  = Process(target=producir, name='productor',  args=(almacen, puertaDejar, puertaRecoger, cambios))
        consumidor = Process(target=consumir, name='consumidor', args=(almacen, puertaDejar, puertaRecoger, cambios))
        
        consumidor.start() #aunque comiencce primero el consumidor, esperará
        productor.start()

    start = Button(frame, text="Start", command=start)
    start.pack()
 
    try:
        while 1:
            if not cambios.empty():
                s = cambios.get()
                if s  == 'quit':
                    break
                else:
                    canvas.itemconfigure(obj[s[0]],fill = s[1])
                    if s[2] == 'quitar':
                        ALMACEN = ALMACEN[:-2]
                    elif s[2] != None:
                        ALMACEN = s[2] + ALMACEN
                    canvas.itemconfigure(textAlmacen, text = ALMACEN)
                    sleep(0.3)
            root.update() 
    except TclError:
        pass