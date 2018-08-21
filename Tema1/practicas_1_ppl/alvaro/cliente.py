from multiprocessing.connection import Client
from multiprocessing import Queue
from multiprocessing import Process
from random import random
from time import sleep
from Tkinter import *
import tkFont

#Esta funcion introduce en la cola  el tablero.

def mostrar_tablero(ventana_queue, tablero):

    """Introduce en la cola el tablero.
    
    Parametros:
    ventana_queue -- cola de la ventana
    tablero -- lista de elementos del tablero

    """
    ventana_queue.put(('tablero', tablero))

#Esta funcion introduce en la cola la respuesta que enviaremos al cliente.

def mostrar_respuesta(ventana_queue, respuesta):

    """Introduce en la cola la respuesta.
    
    Parametros:
    ventana_queue -- cola de la ventana
    respuesta -- tupla con el codigo del estado de movimiento y el tablero actualizado

    """
    ventana_queue.put(('respuesta', respuesta))

#Esta funcion introduce en la cola el tablero final y la respuesta de fin de juego.

def final_juego(ventana_queue, tablero, respuesta):

    """Introduce en la cola el tablero final y la respuesta de fin de juego.
    
    Parametros:
    ventana_queue -- cola de la ventana
    tablero -- lista de elementos del tablero
    respuesta -- tupla con el codigo del estado de movimiento y el tablero actualizado

    """
    ventana_queue.put(('Quit', tablero, respuesta))

#Esta funcion obtiene el movimiento que manda el cliente.

def leer_movimiento(input_queue):

    """Obtiene el movimiento que realiza el jugador.
    
    Parametros:
    input_queue: cola de movimientos

    """

    return eval(input_queue.get())

#Esta funcion pertenece a la creacion de la interfaz grafica.

def interfaz_grafica(ventana_queue, equipo, input_queue):

    """ Abre una ventana a traves del tkinter en la que se realiza el movimiento, muestra el tablero y el estado del movimiento.

    Parametros:
    ventana_queue: cola de mensajes y tablero
    equipo: lista de equipos
    input_queue: cola de movimientos
    
    """
    root = Tk()
    fuente = tkFont.Font(family="Helvetica", size=10) #Elegimos el tipo de letra.

    root.title('Equipo del cliente: ' + str(equipo)) #Ponemos el titulo a la ventana.
    root.resizable(0, 0)

    frame = Frame(root)
    frame.pack()
    
    #Creamos la ventana en la que aparece el tablero y en la que introducimos el movimiento y los letreros que nos los indicaran.

    equipo_label = Label(frame, text="Jugando para el equipo: " + str(equipo), font=fuente) #
    equipo_label.pack()
     
    tablero_juego = Entry(frame, width=50, justify=CENTER , font=fuente)
    tablero_juego.pack()

    input_label = Label(frame, text="Movimiento: ", font=fuente)
    input_label.pack()
    input_value = StringVar()
    input_data = Entry(frame, width=30, justify=CENTER, font=fuente,text=input_value)
    input_data.pack()
    
    def pulsar_boton():
        input_queue.put(input_data.get())
    
    def enter(event):
        pulsar_boton()
    
    #Creamos un boton que al pulsar el raton o el intro envie el movimiento que queremos hacer. 

    input_button = Button(frame, activeforeground="White",activebackground="Black", text="Envia movimiento", justify=CENTER, command=pulsar_boton)
    input_button.pack()
    input_data.bind('<Return>', enter)

    #Creamos la ventana en la que se mostrara si el movimiento se ha realizado o no.

    mensaje = Entry(frame, width=60, justify=CENTER, font=fuente)
    mensaje.pack()
    
    #Actualizamos el tablero y la ventana del mensaje.
    try:
        while 1:
            if not ventana_queue.empty():
                s = ventana_queue.get()
                if s[0] == 'Quit':
                    mensaje.delete(0,END)
                    mensaje.insert(0,s[2])
                    tablero_juego.delete(0,END)
                    tablero_juego.insert(0,s[1])
                elif s[0] == 'tablero':
                    tablero_juego.delete(0,END)
                    tablero_juego.insert(0,s[1])
                    input_data.delete(0,END)
                elif s[0] == 'respuesta':
                    mensaje.delete(0,END)
                    mensaje.insert(0,s[1])
                    input_data.delete(0,END)
            root.update()
    except TclError:
        pass


#Este el programa principal que ira ejecutando las funciones anteriores haciendo que el juego funcione.

print '\n', "Cargando el juego", '\n'
conn = Client(address=('localhost', 6000), authkey='secret password') 
informacion = conn.recv() #Recibimos el estado del tablero y el equipo al que pertenecemos, 0 o 1.
equipo = informacion[0]
fila = informacion[1][0]
columna = informacion[1][1]
tablero = informacion[1][2]


#Creamos dos colas, una para el tablero y la respusta y otra para el movimiento que hacemos.

ventana_queue = Queue() 
input_queue = Queue()

#Lanzamos la ventana de juego.

ventana_tablero = Process(target=interfaz_grafica, args=(ventana_queue,equipo,input_queue))
ventana_tablero.start()

mostrar_tablero(ventana_queue, tablero) #Estado del tablero al comenzar.

mostrar_respuesta(ventana_queue, 'Introduce una tupla de enteros (fila,col) / 0 <= fila < '+str(fila)+', 0 <= col < '+str(columna)) #Mensaje inicial.

print tablero


terminado = False
while not terminado:
    aux = False
    while not aux:
        try:
            movimiento = leer_movimiento(input_queue) #Lee el movimiento que hacemos.
            if ((movimiento[0] or movimiento[1]) >= max(fila,columna)) or ((movimiento[0] or movimiento[1]) < 0):
                conn.send((equipo,1))
            else:
                conn.send((equipo,movimiento)) #Envia el movimiento al listener.
            aux = True
        except SyntaxError:
            mostrar_respuesta(ventana_queue, 'Introduce bien la tupla')
            
    hecho = False
    while not hecho:
        try:
            respuesta = conn.recv() #Recibimos una respuesta en funcion del movimiento que hagamos y del turno en el que este el juego.
            print '\n', "mensaje recibido:", respuesta
            if respuesta[0] == 0: 
                respuesta1 = 'Movimiento hecho'
            elif respuesta[0] == 1:
                respuesta1 = 'Posicion ocupada o erronea, pierde turno'
            elif respuesta[0] == 2:
                respuesta1 = 'Espera turno'
            elif respuesta[0] == 3:
                respuesta1 = 'Fin del juego'
            mostrar_respuesta(ventana_queue, respuesta1)
            if respuesta[0] == 1 or \
               respuesta[0] == 0:
                tablero = respuesta[1][2]
                mostrar_tablero(ventana_queue, tablero)
                hecho = True
            elif respuesta[0] == 3:
                tablero = respuesta[1][2]
                final_juego(ventana_queue, tablero, respuesta1)
                hecho = True
                terminado = True
        except EOFError:
            print '\n', "El servidor ha sido desconectado"
            mostrar_respuesta(ventana_queue, 'El servidor se ha desconectado')
            hecho = True
            terminado = True
print '\n', "Ha salido del juego"
conn.close
