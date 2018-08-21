from multiprocessing import Process
from multiprocessing import Pipe
import random, time

def filosofo(i,canal,tenedor):
    for x in range(10):
        print "Filosofo", i, "piensa...", x
        time.sleep(random.random()/4)

        while not tenedor:
            print "Filosofo", i, "pide tenedor"
            canal.send("Necesito el tenedor, pls")
            if canal.recv()=="El tenedor es tuyo" :
                tenedor = True
                print "Filosofo", i, "recibe tenedor"

        print "Filosofo", i, "come", x
        time.sleep(random.random()/4)

        if canal.poll() :
            if canal.recv()=="Necesito el tenedor, pls":
                tenedor = False
                print "Filosofo", i, "envia tenedor"
                canal.send("El tenedor es tuyo")
                
    if tenedor :
        canal.send("El tenedor es tuyo")

if __name__ == "__main__":

    canal1, canal2 = Pipe()
    f1 = Process(target = filosofo, args=(1,canal1,True))
    f2 = Process(target = filosofo, args=(2,canal2,False))
    f1.start()
    f2.start()
