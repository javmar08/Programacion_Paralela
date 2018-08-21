# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:10:07 2015

@author: alumno
"""
from multiprocessing import Manager
from multiprocessing.connection import Listener
from multiprocessing import Process
from multiprocessing.connection import AuthenticationError
from multiprocessing import Condition
import random

#FUNCION QUE SORTEA EL EQUIPO QUE EMPEZARA A JUGAR
def asignaTurno():
    #guardamos en variable un numero aleatorio entre 1 y 10
    variable = random.randint(1,10)
    #miramos si es par
    #si lo es empezaria a jugar el equipo 0
    #inicializamos una variable que llamamos equipo a 0
    #que sera la que devolvemos
    if variable %2 ==0:
        equipo = 0
    #si no es par el numero que ha salido aleatoriamente
    #le tocaria jugar al equipo 1
    #inicializamos la variable equipo a 1
    else:
        equipo = 1

    return equipo

#FUNCION QUE DADO UN TABLERO TE DICE SI ESTA VACIO O NO
def completo(tablero):
    vacio = False
    i=0
    #Recorreremos el tablero con un while
    while vacio == False and i<len(tablero):
        #Mientras que no encuentre una casilla que este vacia
        #sigo recoriendo la lista
        if tablero[i] != -1:
            i = i +1
        #en cuanto encuentre una casilla que no esta vacia
        #variamos el valor de la variable tablero
        #y saldremos del bucle
        else:
            vacio = True
    #Devolvemos la varible
    return vacio

#FUNCION QUE ESTUDIA LOS CASOS DE LOS POSIBLES MOVIMIENTOS
#QUE TE MANDA UN USUARIO
def ponerFicha (tablero,dim_rows,dim_columns,movimiento,team,conn):
    #Pasamos la variable team para saber que tenemos que añadir en el tablero
    #ya que si el juega el equipo 0 pondremos este valor en el tablero
    #si juega el equipo 1 pondremos este valor en el tablero    
    #movimiento es una lista con dos elementos
    #el primero sera la fila y el segundo la columna donde queremos
    #colocar la ficha
    
    fila = movimiento[0]
    columna = movimiento[1]
    
    #Ahora tenemos que comprobar si en nuestro tablero
    #dicha posicion esta ocupada por
    #una ficha o no
    #Vamos a considerar que hay -1 si la casilla esta vacia
    #Si esta vacia ponemos un 0 si juega el equipo 0
    #y un 1 si juega el equipo 1
    
    #El usuario por pantalla sabe la dimension del tablero por lo que
    #nos da dos valores, la fila y la columna donde quiere poner su ficha
    #para poder acceder a dicha posicion en nuestro tablero que es una lista
    #tenemos que hacer una conversion a numero de esa posicion
    #que se hara de la forma (fila*(numero de columnas)+columna)
    
    #Si la casilla esta vacia
    if tablero[fila*dim_columns+columna] == -1:
        
        #Si le toca al equipo 0
        if team ==0:
            #cambio el valor de dicha casilla por el numero del equipo
            #en el que esta el jugador
            tablero[fila*dim_columns+columna]= 0
            #Mando un 0 como mensaje de que se ha realizado correctamente
            #el movimiento y mando junto a este el tablero
            conn.send((0,(dim_rows,dim_columns,tablero[:])))
            
            #Miramos si el tablero tras nuestro movimiento pasa a estar completo o no
            #llamamos a la funcion que hemos hecho anteriormente
            #que nos devuelve False SI ESTA COMPLETO
            #si esta completo mandamos un 3 y el tablero
            if completo(tablero) == False:
                conn.send((3,(dim_rows,dim_columns,tablero[:])))
            #Si no esta completo vamos a enviarle como respuesta un 4,
            #que no vera el usuario, simplemente lo utilizamos para
            #poder controlar bien el bucle que hara que el juego acabe
            else:
                conn.send((4,(dim_rows,dim_columns,tablero[:])))
            

        #Si juega el equipo 1
        else:
            #cambio el valor de la casilla por un 1
            tablero[fila*dim_columns+columna]= 1
            #Mando un 0 como mensaje de que se ha realizado correctamente
            #el movimiento
            conn.send ((0,(dim_rows,dim_columns,tablero[:])))
            
            #Miramos si el tablero tras nuestro movimiento pasa a estar completo o no
            #llamamos a la funcion que hemos hecho anteriormente
            #que nos devuelve False SI ESTA COMPLETO
            #si esta completo mandamos un 3 y el tablero
            if completo(tablero) == False:
                conn.send((3,(dim_rows,dim_columns,tablero[:])))
            
            #Si no esta completo vamos a enviarle como respuesta un 4,
            #que no vera el usuario, simplemente lo utilizamos para
            #poder controlar bien el bucle que hara que el juego acabe
            else:
                conn.send((4,(dim_rows,dim_columns,tablero[:])))
            
            
    
    #Si la casilla correspondiente a dicho movimiento no esta vacia
    #le devolvemos al jugador un mesaje con un 1 para que sepa que el
    #movimiento no es posible y mandamos tambien el tablero
    else:
        conn.send((1,(dim_rows,dim_columns,tablero[:])))
        
        #Al ser el movimiento erroneo no vamos a comprobar 
        #si nuestro tablero ha sido completado ya que no hemos
        #hecho ningun movimiento
        #procedemos nuevamente a enviarle un 4, dato que no vera el usuario
        #sino que nos servira para controlar cuando acaba el juego
        conn.send((4,(dim_rows,dim_columns,tablero[:])))


#PROCESO
def juego(conn,jugador,turno,dim_rows,dim_columns,tablero,c):
    
    while True:
        #Recibo del usuario su equipo y el movimiento
        #que desea hacer
        (team,movimiento) = conn.recv()
        #Vamos a usar condiciones para controlar la concurrencia
        c.acquire()
        
        #La condicion del while determina cuando voy a esperar.
        #Ponemos como condicion que el valor del turno coincida con el numero
        #del equipo, es decir si el turno es 0 juega el equipo 0 y los jugadores del
        #equipo 1 esperan, y si el turno es 1 jugara el equipo 1 y seran los jugadores
        #del equipo 0 los que esperan.
        while (turno[0] != team):
            #mando un mensaje al jugador de que no es su turno y por tanto 
            #que le toca esperar
            conn.send((2,(dim_rows,dim_columns,tablero[:])))
            #mandamos un 4 para que no se acabe el bucle que hemos creado 
            #en el cliente
            conn.send((4,(dim_rows,dim_columns,tablero[:])))
            c.wait()  
                
        c.release()
        
        #Si realmente si es mi turno no entro en el while
        #y paso a comprobar si el movimiento que me manda el jugador
        #es valido o no
        
        ponerFicha(tablero,dim_rows,dim_columns,movimiento,team,conn)
           
        c.acquire()
        
        #Miramos de quien era el turno y en funcion de quien fuera
        #lo variamos para que pueda jugar el otro equipo
        if turno[0] == 0:
            turno[0] = 1
            #Despierto a aquellos jugadores "dormidos"
            c.notify_all()
        else:
            turno[0]=0
            #Despierto a aquellos jugadores "dormidos"
            c.notify_all()
        c.release()




#FUNCION PRINCIPAL
if __name__=='__main__':
    
    listener = Listener(address=('localhost',6000),authkey = 'secret password')
    print 'listener starting'
    
    c= Condition()
    
    #Usamos un manager para controlar el turno con el que juega cada equipo
    #Para que sea un juego justo y no empieze a jugar siempre el mismo equipo
    #vamos a sortear el turno de comienzo
    #vamos a escoger un numero aleatorio entre 1 y 10
    #si sale un numero PAR el turno ira para el equipo 0
    #si sale un numero IMPAR el turno ira para el equipo 1
    #esto lo determinaremos en una funcion que llamamos asignaTurno
    #y que devuelve un 0 o un 1 en funcion de a quien le toque
    
    manager = Manager()
    turno= manager.list([0])
    
    #una vez creado el turno lo inicializamos a el valor
    #que se elige en el sorteo
    turno[0] = asignaTurno()
    
    #tomamos un N arbitrario para generar el tablero
    #En funcion del numero de jugadores se variará para hacer
    #el juego mas entretenido
    
    N=3
    #Vamos a considerar un tablero de NxN
    #pero el programa esta pensado para cualquier dimension del tablero
    
    #Numero de filas
    dim_rows=N
    
    #Numero de columnas
    dim_columns= N
    
    numero_casillas = N*N
    #Generamos el tablero que estara controlado por un manager
    #para que los cambios se realizen con concurrencia mas facilmente
    #Vamos a poner que inicialmente el tablero esta vacio y cada casilla vacia
    #se representa con un -1
    tablero = manager.list([-1]*numero_casillas)
    
    while True:
        
        try:
            
            #acepto la conexion 
            conn = listener.accept()
            jugador = listener.last_accepted
            print 'connection accepted from', jugador
            
            
            #Vamos a usar dos listas para gestionar el reparto de jugadores en cada equipo
            #en un principio ambas estan vacias y en funcion de su longitud
            #iremos repartiendo los jugadores en una u otra para que
            #ambos equipos esten igualados
            cero=[]
            uno=[]
            
            #si hay mas jugadores en el equipo uno
            #el proximo jugador que llege ira al equipo cero
            if len(cero)<=len(uno):
                cero.append(jugador)
            
                #una vez que hemos añadido el jugador a un equipo
                #le mandamos un mesaje para que este sepa en que equipo esta
                #en este caso 0, es decir esta en el equipo 0 y el tablero con el que juega
                #al ser tablero controlado por un manager no podemos enviarlo tal cual
                #para enviar sus elementos usamos tablero [:]
                team = 0
                conn.send((team,(dim_rows,dim_columns,tablero[:])))
            
            #si hay mas jugadores en el equipo cero
            #el siguiente jugador ira al equipo uno
            else:
                uno.append(jugador)
                #una vez añadido el jugador al equipo
                #le mandamos un mensaje al usuario para que este sepa en que equipo esta
                #igual que en el caso anterior mandamos tambien el tablero
                #para solucionar el problema del manager ponemos tablero[:]
                team = 1
                conn.send((team,(dim_rows,dim_columns,tablero[:])))
        
            #hacemos un for para recorrer la lista de jugadores
            #del equipo blanco y del equipo negro y ejecutamos el proceso
            #por cada uno de ellos
            
            for i in cero:
                p = Process(target=juego, args=(conn,listener.last_accepted,turno,dim_rows,dim_columns,tablero,c))
                p.start()
        
            for j in uno:
                p=Process(target=juego, args=(conn,listener.last_accepted,turno,dim_rows,dim_columns,tablero,c))
                p.start()
            
        
        except AuthenticationError:
            print 'Connection refused, incorrect password'
        
print 'programa finalizado'     
