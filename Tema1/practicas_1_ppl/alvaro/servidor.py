from multiprocessing.connection import Listener
from multiprocessing import Process
from multiprocessing.connection import AuthenticationError
from multiprocessing import Condition
from multiprocessing import Manager
from multiprocessing import Queue
from Tkinter import *
import tkFont
import time, random

# Politica de acceso al tablero, se hacen dos equipos el 0 y 1 segun la entrada de los jugadores. 
# El primero que entra va al 0, el segundo al 1 y asi alternandose.
# Si algun cliente se desconecta se mantendra esta politica de entrada a pesar de que se pueda quedar un jugador solo.
# No importa que se quede solo, pues aunque jugaria contra un equipo mayor, hay una alternancia de turnos.
# Primero enviara movimiento el equipo 0, y posteriormente uno y solo uno del equipo 1. 
# Si varios enviasen, se ejecutaria el mas rapido quedando los otros en espera y a que un jugador del equipo 0 haga su movimiento.
# Si un jugador intenta poner en una posicion que esta ocupada, se le saltaria el turno. 
# Si tiene un error de tipo al introducir su movimiento, tambien perderia el turno. 
# Las ventajas de este metodo es que aunque juegue un jugador contra 10, se entenderia como 1 contra 1. 
# Las desventajas es que los jugadores mas lentos o torpes podrian quedarse sin jugar. 
# El jugador sera una vez acabado el juego quien cuente quien ha ganado.
# El tablero esta iniciado con "-1" y si hace un movimiento el equipo 0 o el 1 se sutituira por un "0" o un "1" respectivamente.
# Las listas del tablero y turnos estan controladas con el modulo Manager de multiprocesiing.


def dibujo_tablero(fila,columna,tablero):
    """ Devuelve en la terminal un tablero 2D.
    
    Parametros:
    fila --  numero de filas del tablero
    type fila -- Int
    columna -- numero de columnas del tablero
    type columna -- Int
    tablero -- lista con los elementos del tablero
    type tablero -- List

    """
    i = 0
    while i < (fila*columna):
        print tablero[i:columna+i]
        i = i + columna 

#Esta funcion devolvera u

def movimiento(fila, columna, movimiento, tablero):

    """Modifica el tablero segun el movimiento realizado y devuelve una tupla sobre el estado del movimiento.
    Devuelve 1 si el movimiento es erroneo o la casilla ya esta ocupada
    Devuelve 3 si el tablero esta completo y el juego ha finalizado
    Devuelve 0 si el movimiento se ha hecho con exito
    
    Parametros:
    fila --  numero de filas del tablero
    type fila -- Int
    columna -- numero de columnas del tablero
    type columna -- Int
    movimiento -- tupla con informacion del equipo y el movimiento realizado por el cliente
    type movimiento -- Tuple
    tablero -- lista con los elementos del tablero
    type tablero -- List 
    
    Excepciones:
    TypeError -- Si se recibe un tipo erroneo de movimiento
    IndexError -- Si se recibe un movimiento con un indice de lista de tablero incorrecto

    """
    try:
        posicion = fila*movimiento[1][0]+movimiento[1][1]
    except TypeError:
        return (1,(fila, columna, tablero))
    try:
        if (tablero[posicion] == 0 or tablero[posicion] == 1):
            if type(final_juego(fila, columna, tablero)) == tuple:
                return (3, (fila, columna, tablero))
            else:
                return (1, (fila, columna, tablero))
        else:
            if movimiento[0] == 0:
                tablero[posicion] = 0
            elif movimiento[0] == 1:
                tablero[posicion] = 1
            if type(final_juego(fila, columna, tablero)) == tuple:
                return (3, (fila, columna, tablero))
            else:
                return (0, (fila, columna, tablero))
    except IndexError:
        return (1,(fila, columna, tablero))


def final_juego(fila, columna, tablero):

    """ Indica si el tablero esta completo.
    
    Parametros:
    fila --  numero de filas del tablero
    type fila -- Int
    columna -- numero de columnas del tablero
    type columna -- Int
    tablero -- lista con los elementos del tablero
    type tablero -- List

    """
    aux = True
    i = 0
    while (i < len(tablero)) and aux:
        if tablero[i] == -1:
            aux = False
        i = i + 1
    if (i == len(tablero)) and (tablero[i-1] != -1):
        print "El juego ha terminado"
        return (3,(fila, columna, tablero))
    else: 
        pass


def servidor(c, cliente, id, equipo, turno):

    """Se encarga de manejar la participiacion de los diferentes clientes por turnos.
    Ademas de enviar al cliente el estado de su movimiento

    Parametros:
    c -- encargado de gestionar los turnos mediante el modulo Condition de multiprocessing
    cliente -- conexion establecida con el cliente
    id -- tupla con la identidad del cliente que se une al juego
    equipo -- lista [0,1] que indica los dos equipos que existen
    turno -- lista [0,1] que indica a quien pertenece el turno

    Excepcion:
    EOFError -- Si el cliente se desconecta

    """    
    aux = True
    while aux:
        try:
            movimiento_cliente = conn.recv()
            print id, 'quiere poner en', movimiento_cliente
            realizado = False
            c.acquire()
            while (turno[0] != movimiento_cliente[0]) and not final_juego(fila, columna, tablero):
                conn.send((2,(fila, columna, tablero)))
                c.wait()
            if (turno[0] == equipo[0]):
                envio = movimiento(fila, columna, movimiento_cliente, tablero)
                dibujo_tablero(fila, columna, tablero)
                turno[0] = 1
                conn.send(envio)
            elif (turno[0] == equipo[1]):
                envio = movimiento(fila, columna, movimiento_cliente, tablero)
                dibujo_tablero(fila, columna, tablero)
                turno[0] = 0
                conn.send(envio)
            c.notify_all()            
            c.release()
        except EOFError:
            print 'El cliente', id, 'se ha desconectado'
            aux = False
            

#Programa principal que inicia el tablero, recibe los clientes e inicia sus procesos.

if __name__ == "__main__":

    listener = Listener(address=('localhost', 6000), authkey='password')
    aux = 1
    equipo = [0,1]
    equipo_0 = []
    equipo_1 = []

    manager = Manager()
    turno = manager.list([0])
    c = Condition()
    print '\n', "Cargando juego", '\n'

    tablero = manager.list([])
    while True:
        try:
            fila = int(raw_input('Cuantas filas quieres?: '))
            columna = int(raw_input('Cuantas columnas quieres?: '))
            break
        except ValueError:
            print '\n', "Tiene que introducir un entero para la fila y otro para la columna.", '\n'
    for i in range(fila*columna):
                tablero.append(-1)
    
    print '\n', 'Este es el tablero de juego:', '\n'
    dibujo_tablero(fila,columna,tablero)

    while True:
        print '\n', "Aceptando jugadores"
        try: 
            conn = listener.accept()
            print '\n',"Ha entrado al juego", listener.last_accepted
            if (aux == 1):
                equipo_0.append(listener.last_accepted)
                conn.send((0,(fila,columna,tablero)))
                aux = 0
                serve = Process(target=servidor,args=(c, conn, listener.last_accepted, equipo, turno))
                serve.start()
                print '\n', "Equipo 0: ",equipo_0, "\n", "Equipo 1: ", equipo_1

            elif (aux == 0):
                equipo_1.append(listener.last_accepted)
                conn.send((1,(fila,columna,tablero)))
                aux = 1
                serve = Process(target=servidor,args=(c, conn, listener.last_accepted, equipo,  turno))
                serve.start()
                print '\n', "Equipo 0: ",equipo_0, "\n", "Equipo 1: ", equipo_1
        
        except AuthenticationError:
            print "El jugador no ha podido entrar"
