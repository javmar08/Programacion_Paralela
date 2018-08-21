# -*- coding: utf-8 -*-

from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError
from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import Manager
from time import sleep

def fin_juego(dim_filas, dim_columnas, estado_tablero):
    # Comprobar si el juego ha terminado
    r = 0
    for i in range(dim_filas * dim_columnas):
        if estado_tablero[i] == -1:
            r = 1
    if r == 0:
        resultado = True
    else: resultado = False
    return resultado

def envio(conn, equipo_resultado, dim_filas, dim_columnas, estado_tablero):
    # envio de mensajes
    conn.send((equipo_resultado, (dim_filas, dim_columnas, estado_tablero)))
    print '((', equipo_resultado, '(', dim_filas, ',', dim_columnas, ',', estado_tablero, '))'

def t(condicion, turno, T, juego_ha_empezado, juego_ha_terminado):
    while not juego_ha_terminado[0]:
        sleep(T)
        
        # Si el juego ha empezado cada T segundos cambiamos el turno
        if juego_ha_empezado[0]:
            print 'libero a todos y cambio turno'
            condicion.acquire()
            if turno[0] == 0: turno[0] = 1
            else: turno[0] = 0
            condicion.notify_all()
            condicion.release()

def f(conn, listener, codicion, dim_filas, dim_columnas, estado_tablero, turno, jugadores, equipo, juego_ha_terminado):
    # proceso para cada jugador
    
    # envío 1er mensaje a cliente
    envio(conn, equipo, dim_filas, dim_columnas, estado_tablero[:])
    
    # esperamos jugada
    while True:
        try:
            data_recv = conn.recv()
        except EOFError:
            print 'abandona un jugador del equipo', equipo
            jugadores[equipo] = jugadores[equipo] - 1
            break
        
        jugada_equipo = data_recv[0]
        jugada = data_recv[1]
        posicion = jugada[0] * dim_columnas + jugada[1]
            
        if not (posicion >= 0 and posicion < dim_filas * dim_columnas):
            print 'jugada ilegal del equipo', equipo, ', jugador expulsado'
            jugadores[equipo] = jugadores[equipo] - 1
            break
        
        saliendo_de_espera = False
        condicion.acquire()
        # La condición para esperar será o no es el turno de mi equipo o el juego no ha empezado
        while ((turno[0] != jugada_equipo) or (not juego_ha_empezado[0])):
            if fin_juego(dim_filas, dim_columnas, estado_tablero[:]): resultado = 3
            else: resultado = 2
            envio(conn, resultado, dim_filas, dim_columnas, estado_tablero[:])
            condicion.wait()
            saliendo_de_espera = True
        condicion.release()
            
        if not saliendo_de_espera:    
            # Comprobamos si la jugada es valida 
            if estado_tablero[posicion] == -1:
                estado_tablero[posicion] = jugada_equipo
                resultado = 0
            else:
                resultado = 1
            if fin_juego(dim_filas, dim_columnas, estado_tablero[:]):
                juego_ha_terminado[0] = True
                resultado = 3
            envio(conn, resultado, dim_filas, dim_columnas, estado_tablero[:])
          
    conn.close()

if __name__ == '__main__':
    listener = Listener(address=('localhost', 6000), authkey='secret')

    # Valores fijos durante el juego
    # tiempo en segundos para cambiar de turno
    T = 5
    # dimesión del tablero, filas
    dim_filas = 2
    # dimesión del tablero, columnas
    dim_columnas = 3
    # Jugadores iniciales para comenzar partida
    jugadores_iniciales = 2

    # Definimos los recursos compartidos
    manager = Manager()
    turno = manager.list([0])
    estado_tablero = manager.list([-1] * dim_filas * dim_columnas)
    jugadores = manager.list([0,0])
    juego_ha_empezado = manager.list([False])
    juego_ha_terminado = manager.list([False])
    condicion = Condition()

    # Controlamos el cambio de turno desde este proceso
    pt = Process(target=t, args=(condicion, turno, T, juego_ha_empezado, juego_ha_terminado))
    pt.start()

    print 'Esperando jugadores'

    while True:
        try:
            conn = listener.accept()
        except AuthenticationError:
            print 'Error en las credenciales', listener.last_accepted
            
        print 'Nuevo jugador desde', listener.last_accepted
      
        # Asignamos equipo al jugador, el primero será al equipo0 para asegurar al menos 2 jugadores
        if (jugadores[0] > jugadores[1]):
            equipo = 1
            jugadores[1] = jugadores[1] + 1
        else:
            equipo = 0
            jugadores[0] = jugadores[0] + 1

        # aqui creamos un nuevo proceso por cada jugador 
        p = Process(target=f, args=(conn, listener, condicion, dim_filas, dim_columnas, estado_tablero, turno, jugadores, equipo, juego_ha_terminado))
        p.start()
        
        # Si el número de jugadores es igual o mayor que jugadores_iniciales comienza el combate
        if ((jugadores[0] + jugadores[1] >= jugadores_iniciales) and (not juego_ha_empezado[0])):
            juego_ha_empezado[0] = True
            print 'Comienza el combate', juego_ha_empezado[0]
        elif ((jugadores[0] + jugadores[1] < jugadores_iniciales) and (not juego_ha_empezado[0])):
            print 'Aún queda(n)', jugadores_iniciales - (jugadores[0] + jugadores[1]), 'jugador(es) para empezar el combate'

    listener.close()

'''
Comentarios de la práctica
por David González López-Tercero

Esta es una de las muchas alternativas que he ido probando, queda como un buen esqueleto para adaptar
    a este u otro problema

He creado 4 constantes que definen:
- Tamaño del tablero: dim_filas y dim_columnas
- Tiempo en segundos para cambiar de turno: T
- Número de jugadores iniciales necesarios para comenzar el combate: jugadores_iniciales

Las siguientes variables gestionadas por un manager, he escogido en todas ellas listas (aún con un único elemento)
    por su sencilled y buen comportamiento con los manager:
- turno = manager.list([0]), indica si el turno es del equipo0 turno[0] = 0 o del equipo1, turno[0] = 1
- estado_tablero = manager.list([-1] * dim_filas * dim_columnas), estado del tablero, -1 libre, 0 equipo0, 1 equipo1
- jugadores = manager.list([0,0]), número de jugadores en cada equipo, jugadores[0] equipo0, jugadores[1] equipo1
- juego_ha_empezado = manager.list([False]), controlamos si el combate ha empezado, juego_ha_empezado[0] = True
- juego_ha_terminado = manager.list([False]), controlamos si hemos terminado, juego_ha_terminado[0] = True
    Aquí hay que hacer notar que nuestro servidor no termina de atender a nuevos jugadores nunca aunque podría
    ya que controlamos este evento ya que por las limitaciones de nuestro protocolo hacerlo implicaría que todos los
    demás jugadores que no han realizado la última jugada no se enterarían de quién ha ganado, ni siquiera si hemos
    terminado ya que sólo reciben información del juego cuando envián una nueva jugada al servidor y éste les contesta

Una condición: condicion, para controlar el turno, poner es espera a todos hasta que empiece el combate y
    a los que ya empezado el combate quieran jugar y no sea su turno

Un proceso p por cada nuevo jugador que espera jugada y responde a ésta, (jugada -> respuesta)

Un único proceso pt que se encargará de una vez que comience el combate ir cambiando el turno cada T segundos 

El juego comenzará cuando se alcanze el número de jugadores iniciales
los jugadores se van asignando a cada equipo según el número de componentes en cada uno, rellenando el más vacío
Por otra limitación del protocolo elegido, cuando un jugador tiene que esperar el servidor se lo notifica con un 2,
    si ejecutaramos la jugada que le llevó a esperar cuando despierta tendríamos un problema ya que el cliente
    recibiría 2 mesajes seguidos del servidor (jugada -> respuesta1 + respuesta2), esto no es díficil de codificar
    pero rompe con lo definido, (jugada -> respuesta), en nuestro protocolo por tanto en aras de que tanto servidor
    como cliente funcionen con cualquier otro desarrollo he decidido que la jugada que llevó a la espera se pierde,
    también probé a ignorar la siguiente jugada que mande el cliente y ejecutar la vieja que le dejó en espera pero
    al cliente le da la impresión de que el servidor se volvió loco y no me gusta

Si un cliente corta la comunicación o intenta una jugada ilegal se le expulsará de su equipo dejando esa vacante libre    
'''