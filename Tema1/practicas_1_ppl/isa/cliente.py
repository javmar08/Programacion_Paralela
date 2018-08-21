# -*- coding: utf-8 -*-

from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing.connection import Client

from random import random
from time import sleep
from Tkinter import *
import tkFont

def show_board(window_queue, gameboard):
    window_queue.put(('board',gameboard))

def show_answer(window_queue, answer):    
    window_queue.put(('answer',answer))

def read_movement(input_queue):
    return eval((input_queue.get()))


def graphical_interface(board_queue,team,input_queue,filas,columnas):
    root = Tk()
    my_font = tkFont.Font(family="Helvetica", size=24)

    root.title('Cliente of team '+str(team))
    root.resizable(0, 0)

    frame = Frame(root)
    frame.pack()
    
    #ETIQUETAS
    tablero_label = Label(frame, text='TABLERO DE: '+str(columnas)+' COLUMNAS - '+str(filas)+' FILAS' ,font=my_font)
    tablero_label.pack()
    gameboard = Entry(frame,width=67,font=my_font)
    gameboard.pack()
    input_label = Label(frame, text="Movimiento", font=my_font)
    input_label.pack()
    input_value = StringVar()
    input_data = Entry(frame,width=5,font=my_font,textvariable=input_value)
    input_data.pack()
    def press_button():
        #Pongo en la cola los datos que recibo
        input_queue.put(input_data.get()) 
            
    input_button = Button(frame, text="Envía movimiento", command=press_button)
    input_button.pack()
    message = Entry(frame,width=40,font=my_font)
    message.pack()

    try:
        while 1:
            if not board_queue.empty():
                s = board_queue.get()
                if s  == 'quit':
                    break
                elif s[0] == 'board':
                    gameboard.delete(0,END)
                    gameboard.insert(0,s[1])
		elif s[0] == 'answer':
		    message.delete(0,END)
		    message.insert(0,s[1])
            root.update() 
    except TclError:
        pass 



print 'Trying to connect'

conn = Client(address=('localhost',6000), authkey='password')#'secret password') 
#Recibo lo que me manda el listener
(team,gameboard) = conn.recv() 
columnas = gameboard[0]
filas = gameboard[1]
#Cola que gestiona la ventana
window_queue = Queue() 
#Cola que gestiona los datos que intruduce el usuario
input_queue = Queue()
#proceso que se encarga del interfaz grafico
gameboard_window = Process(target=graphical_interface, args=(window_queue,team,input_queue,filas,columnas)) 
#iniciamos el proceso
gameboard_window.start()
show_board(window_queue, gameboard[2])


terminate = False
while not terminate:
    #almaceno en movement el movimiento que ha pasado el jugador por pantalla
    movement = read_movement(input_queue)
    #envio al servidor el equipo del que soy 
    #y el movimiento que quiero hacer
    conn.send((team, movement))
    done = False
    while not done:
        #recibo una respuesta del servidor
        (answer,gameboard) = conn.recv()
        #Guardo en varible un valor que me envia el listener
        #esta nos dira cuando el tablero esta completo y por lo tanto acaba el juego
        #a la vez nos envia el tablero para cumplir con los protocolos establecidos
        #esta variable sera 3 si el tablero queda completado tras el ultimo movimiento
        #esta variable sera 4 si el tablero no queda completado
        (variable,tablero) = conn.recv()
        print 'Received message:', answer
        show_answer(window_queue,answer)
        #Si la respuesta que recibo es 0---> Movimiento realizado correctamente
        #Si la respuesta que recibo es 1 ---> Posicion ya ocupada
        if answer == 0 or answer == 1:
            #enseño el tablero por pantalla
            show_board(window_queue, gameboard[2])
            done = True
    
    #Antes de volver al primer while que supondria que se inicia otra jugada
    #vamos a comprobar si nuestro tablero se ha completado
    #para ello miramos lo que vale el valor variable.
    if variable ==3:
        print 'Received message: ',variable
        show_answer(window_queue,variable)
        terminate = True


       
#Ahora miramos quien de los dos equipos ha ganado
#para ello vamos a recorrer tablero y vemos si hay mas 0's o 1's
#llevaremos dos variables contador0 y contador1
#y luego las compararemos
tablero = gameboard[2]
contador0 = 0
contador1 = 0

for i in tablero:    
    if tablero[i] == 0:
        
        contador0 = contador0 + 1
    else:
        contador1 = contador1 + 1


#Una vez que ya hemos contado cuantos 0's y 1's hay
#miramos que contador es mas grande
#y decimos quien es el ganador
if contador0 > contador1:
    respuesta = 'Team',0,'wins'
    show_answer(window_queue,respuesta)

if contador0 < contador1:
    respuesta = 'Team',1,'wins'
    show_answer(window_queue,respuesta)

if contador0 == contador1:
    respuesta = 'No one wins'
    show_answer(window_queue,respuesta)


print 'Client exits'
conn.close()