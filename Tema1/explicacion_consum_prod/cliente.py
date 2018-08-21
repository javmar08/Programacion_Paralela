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
        return int(input_queue.get())


def graphical_interface(board_queue,team,input_queue):
    root = Tk()
    my_font = tkFont.Font(family="Helvetica", size=24)

    root.title('Cliente of team '+str(team))
    root.resizable(0, 0)

    frame = Frame(root)
    frame.pack()

    team_label = Label(frame, text="Jugando para el equipo "+str(team), font=my_font)
    team_label.pack()
    gameboard = Entry(frame,width=67,font=my_font)
    gameboard.pack()
    input_label = Label(frame, text="Movimiento? ", font=my_font)
    input_label.pack()
    input_value = StringVar()
    input_data = Entry(frame,width=5,font=my_font,textvariable=input_value)
    input_data.pack()
    def press_button():
            input_queue.put(input_data.get())
    input_button = Button(frame, text="envía movimiento", command=press_button)
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




"apatir de aqui seria lo que es el main"
print 'Trying to connect'
#conn = Client(address=('147.96.18.215', 6000), authkey='secret')

conn = Client(address=('localhost', 6000), authkey='secret')
team = conn.recv()
gameboard = conn.recv()

window_queue = Queue()
input_queue = Queue()
gameboard_window = Process(target=graphical_interface, args=(window_queue,team,input_queue))
gameboard_window.start()
show_board(window_queue, gameboard)

terminate = False
while not terminate: # while true
	movement = read_movement(input_queue)
	conn.send((team, movement))
        done = False # done es True cuando pase 'movement done' o cuando
                     # 'position already in use'
        while not done:
            # este bucle es para que espere.
        
                answer = conn.recv()
                print 'Received message:', answer
                show_answer(window_queue,answer)
                if answer == 0 or \ # en el servidor hemos puesto 0
                   answer == 1: # en el servidor envia 1
                        gameboard = conn.recv()
                        show_board(window_queue, gameboard)
                        done = True
print 'Client exits'
conn.close()
