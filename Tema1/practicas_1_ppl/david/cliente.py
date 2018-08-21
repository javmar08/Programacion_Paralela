# -*- coding: utf-8 -*-

from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing.connection import Client
from Tkinter import *
import tkFont

def show_board(window_queue, gameboard):
        window_queue.put(('board',gameboard))

def show_answer(window_queue, answer):
        window_queue.put(('answer',answer))

def read_movement(input_queue):
        data = input_queue.get()
        if data.isdigit(): return int(data)
        else: return -1

def graphical_interface(board_queue,team,input_queue):
    root = Tk()
    my_font = tkFont.Font(family="Helvetica", size=24)

    root.title('Cliente del equipo '+str(team))
    root.resizable(0, 0)

    frame = Frame(root)
    frame.pack()

    team_label = Label(frame, text="Jugando para el equipo " + str(team), font=my_font)
    team_label.pack()
    gameboard = Entry(frame, width=67, font=my_font)
    gameboard.pack()
    input_label = Label(frame, text="Movimiento? ", font=my_font)
    input_label.pack()
    input_value = StringVar()
    input_data = Entry(frame, width=5, font=my_font, textvariable=input_value)
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

if __name__ == '__main__':

    print 'Conectando'
    conn = Client(address=('localhost', 6000), authkey='password')#secret

    # Recibimos los parámetros del juego
    data_recv = conn.recv()
    team = data_recv[0]
    dim_filas = data_recv[1][0]
    dim_columnas = data_recv[1][1]
    gameboard = data_recv[1][2]
    
    window_queue = Queue()
    input_queue = Queue()
    gameboard_window = Process(target=graphical_interface, args=(window_queue, team, input_queue))
    gameboard_window.start()
    show_board(window_queue, gameboard)
    
    terminate = False
    while not terminate:
        # Enviamos jugada si está dentro del tablero
        movement_ok = False
        while not movement_ok:
            movement = read_movement(input_queue)
            if (movement >= 0 and movement < dim_filas * dim_columnas):
                movement_ok = True
        
        movement_x = movement / dim_columnas
        movement_y = movement % dim_columnas
        conn.send((team, (movement_x, movement_y)))
        
        done = False
        while not done:
            data_recv = conn.recv()
            answer = data_recv[0]
            dim_filas = data_recv[1][0]
            dim_columnas = data_recv[1][1]
            gameboard = data_recv[1][2]
                
            print 'Recibida contestación:', answer
            show_answer(window_queue, answer)
            if answer == 0:
                answer_str = "Buena jugada"
            if answer == 1:
                answer_str = "Casilla ocupada"
            if answer == 2:
                answer_str = "No es tu turno"
            if answer == 3:
                contador_equipo0 = 0
                contador_equipo1 = 0 
                for i in range(dim_filas * dim_columnas):
                    if gameboard[i] == 0:
                        contador_equipo0 = contador_equipo0 + 1
                    else:
                        contador_equipo1 = contador_equipo1 + 1
                if contador_equipo0 > contador_equipo1: answer_str = "GANA EL EQUIPO 0"
                elif contador_equipo0 < contador_equipo1: answer_str = "GANA EL EQUIPO 1"
                else: answer_str = "AMBOS EQUIPOS EMPATAN"
            show_board(window_queue, gameboard)
            show_answer(window_queue, answer_str)
            done = True                        

print 'Jugador abandona'
conn.close()
