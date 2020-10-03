#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AEstrella import generate_map,search_position_of,Nodo,a_star
import numpy as np
from time import time
import random as rd
import math
import matplotlib
import matplotlib.pyplot as plt

#Crear API REST con Hug
import hug
    
@hug.get()
def fitness(P_list,map): #calcula el fitness de cierto orden de una lista
    aux = P_list[:]
    f_total = 0
    aux.insert(0,0) #posicion inicial y final son (0,0), es lo que devuelve search_position_of al pasarle un 0
    aux.insert(len(aux),0)
    for j in range(len(aux)-1):
        f_total += len(a_star(map,aux[j],aux[j+1]))
    return f_total

@hug.get()
def swap_positions(current):
    swap1 = rd.choice(current)
    swap2 = rd.choice(current)
    while swap1 == swap2:
        swap2 = rd.choice(current) #por si coinciden
    next=current[:]
    a, b = next.index(swap1), next.index(swap2)
    next[b], next[a] = next[a], next[b]
    return next

@hug.get()
def plot_solution(time_list,prob_list):
    fig, ax = plt.subplots()
    ax.plot(time_list, prob_list)
    ax.set(xlabel='Tiempo', ylabel='Probabilidad')
    ax.grid()
    plt.show()      

@hug.get()
def simulated_annealing(picking_list,order=[m for m in range(1,49)],want_to_print=True):
    map=generate_map(order)
    time=1
    max_time = T = 1000 #coincide con la T inicial
    prob_list = [] #para plotear
    time_list = [] #para plotear
    current = picking_list[:]
    if want_to_print:
        print("Distancia inicial:",fitness(picking_list,map),"con lista:",picking_list)
    #----------Fin de inicializacion de variables----------
    while True:
        T = 0.92*T #decrecimiento exponencial
        if T<0.1 or time > max_time:
            dist_min = fitness(current,map)
            if want_to_print:
                #plot_solution(time_list,prob_list)
                print("Distancia minima:",dist_min,"con lista:",current)
            return dist_min
        
        next = swap_positions(current) #vecino random 
        
        f_next = fitness(next,map)
        f_current = fitness(current,map)
        delta_E = f_next - f_current 

        value = rd.random()             #nro aleatorio entre 0 and 1
        prob = math.exp(-delta_E/(1*T)) 
        if delta_E <= 0:
            current = next
        elif value < prob:
            current = next
            prob_list.append(prob)
            time_list.append(time)
        time+=1

