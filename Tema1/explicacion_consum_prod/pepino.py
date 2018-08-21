from multiprocessing.connection import Listener

from multiprocessing import Process,Lock

listener= Listener(address=('192.168.1.35', 6000),authkey='secret password')

def recibidor(conexion,cliente,equipo,tablero,semaf):
    conexion.send(' La situacion del tablero es: ')
    conexion.send(tablero)
    while not estaLleno(tablero):
        conexion.send(' La situacion del tablero es: ')
        conexion.send(tablero)
        conexion.send('donde deseas poner ficha ')
        m=conexion.recv()
        
        if m = 'quit':
            break
        else:
            semaf.acquire()
            (tablero,caso)=pon(equipo,tablero,m)
            print 'el jugador', cliente,'del equipo',equipo,'quiere poner ficha en', m
            
            semaf.release()
            if caso:
                conexion.send('tu ficha ha sido puesta')
            else:
                conexion.send('no puedes poner en esa casilla')
    conexion.close()

equipo = True
tablero= []
semaf=Lock()
while True:
    conexion= listener.accept()
    
    print 'Se ha conectado', listener.last_accepted
    
    conexion.send(equipo)
    p= Process(target=recibidor,args=(conexion,listener.last_accepted,equipo,tablero,semaf))
    p.start()
    equipo=not equipo
listener.close()
    