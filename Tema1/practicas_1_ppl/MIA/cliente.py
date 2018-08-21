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
        return (input_queue.get())


def graphical_interface(board_queue,team,input_queue,conn):    
    root = Tk()
    my_font = tkFont.Font(family="Helvetica", size=24)
    my_font2 = tkFont.Font(family='Blue', size=20)

    root.title('Cliente of team '+str(team))
    root.resizable(0, 0)

    frame = Frame(root)
    frame.pack()

    team_label = Label(frame, text="Jugando para el equipo "+str(team)+' el tablero es 4X4 enviar el movimiento asi [fila,columna]', font=my_font)
    team_label.pack()
    gameboard = Entry(frame,width=67,font=my_font)
    gameboard.pack()
    input_label = Label(frame, text="Movimiento, [fila,columna] ", font=my_font)
    input_label.pack()
    input_value = StringVar()
    input_data = Entry(frame,width=5,font=my_font,textvariable=input_value)
    input_data.pack()
    def press_button():
            input_queue.put(input_data.get())
    input_button = Button(frame, text="envía movimiento", command=press_button)
    input_button.pack()
    #aqui
    input_label2 = Label(frame, text="¿TE QUIERES IR? ESCRIBE 05 ", font=my_font)
    input_label3 = Label(frame, text="se cerrara la ventana en tu turno ", font=my_font2)
    input_label2.pack()
    input_label3.pack()
    input_value2 = StringVar()
    input_data2 = Entry(frame,width=5,font=my_font,textvariable=input_value2)
    input_data2.pack()
    def press_button2():
        input_queue.put(input_data2.get())
        
    input_button2 = Button(frame, text="desconectarse", command=press_button2)
    input_button2.pack()
    #fin
    message = Entry(frame,width=40,font=my_font)
    message.pack()

    try:
        while 1:
            if not board_queue.empty():
                s = board_queue.get()
                if s[0]  == 'DESCONECTAR':
                    conn.close()
                    root.quit()
                elif s[0] == 'board':
                    gameboard.delete(0,END)
                    gameboard.insert(0,s[1])
		elif s[0] == 'answer':
		    message.delete(0,END)
		    message.insert(0,s[1])
            root.update() 
    except TclError:
        pass 




"apatir de aqui seria lo que es el main"
print 'Trying to connect'

conn = Client(address=('localhost', 6000), authkey='secret')
team = conn.recv()
gameboard = conn.recv()
window_queue = Queue()
input_queue = Queue()
gameboard_window = Process(target=graphical_interface, args=(window_queue,team,input_queue,conn))
gameboard_window.start()
show_board(window_queue, gameboard)

i=0
while i==0:
    movement=read_movement(input_queue)
    print movement    
    conn.send((team,movement))
    done=False
    while not done:
        answer = conn.recv()
        print 'mensaje recibido'
        show_answer(window_queue,answer)
        
        if answer == 'movimiento realizado' or answer == 'esa posicion ya estaba cogida':
            gameboard =  conn.recv()
            show_board(window_queue,gameboard)
            done=True
            
        elif answer == 'fin de la partida, pulsar otra vez a enviar para saber quien ha ganado':
            print 'FIN'
            answer=conn.recv()
            show_answer(window_queue,answer)
            done=True
        elif answer == 'desconectar':
            i=1
            done=True
            
print 'ADIOS'
conn.close()
gameboard_window.terminate()

            
            


