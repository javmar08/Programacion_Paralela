# -*- coding: utf-8 -*-
"""
Mutual exclusion problem solution with non blocking semaphores and active waiting
"""
import time
import random

from multiprocessing import Process, BoundedSemaphore, current_process

N_non_critic = 5
N_critic = 5

def delay(factor=3):
    """ Just to propiciate interleaving """ 
    time.sleep(random.random()/factor)

def non_critic_section():
    p = current_process()
    for i in range(N_non_critic):
        print p.name, "in non critic section", "(%i/%i)"%(i,N_non_critic)
        delay()

def critic_section():
    p = current_process()
    for i in range(N_critic):
        print p.name, "in CRITIC section", "(%i/%i)"%(i,N_critic)
        delay()

def task(semaphore):
    non_critic_section()
    
    while not semaphore.acquire(False):
        print current_process().name, "waiting..."
        delay(factor=6)
    
    critic_section()
    semaphore.release()


if __name__ == '__main__':    
    names = ["Ana","Eva","Pi","Pam","Pum"]
    jobs = []
    K = 2
    semaphore = BoundedSemaphore(K)
    for x in names:
        jobs.append(Process(target=task, name=x, args=(semaphore,)))
    for p in jobs:
        p.start()   
    

               
