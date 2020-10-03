#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Individuo: almacen con cierta disposicion de productos
#Genes: disposicion de productos (48)
#Fitness: distancia de recocido simulado

from TempleSimulado import simulated_annealing,generate_map
import random as rd
import numpy as np
from time import time

#Crear API REST con Hug
import hug

class Individuo():
    def __init__(self,genes=[],fitness=0):
        self.genes = genes
        self.fitness = fitness

@hug.get()
def crear_lista_picking():
    picking_list = []
    all_PL = []                          
    print("Ordenes ficticias: ")
    for i in range(5):                   #lista de 5 listas de picking 
        for j in range(rd.randint(4,8)): #lista de picking variable entre 4 y 8
            value = rd.randint(1,48)     #valor a buscar aleatorio
            if value not in picking_list:#en caso de repetirse busca un nuevo valor
                picking_list.append(value)
        all_PL.append(picking_list)
        print(picking_list)
        picking_list = []
    return all_PL 

@hug.get()
def generar_primer_poblacion(n_poblacion):
    poblacion = []                      #poblacion es una lista de objetos Invidividuo
    for i in range(n_poblacion):
        genes = []
        for j in range(48):
            producto = rd.randint(1,48) #incluye los extremos 1 y 48
            while producto in genes:
                producto = rd.randint(1,48)
            genes.append(producto)
        poblacion.append(Individuo(genes,0)) #pasa de ser una lista a objeto Individuo que contiene esa lista
    return poblacion

@hug.get()
def calcular_fitness(lista,individuo): #individuo ordena nuevamente el mapa en esa disposicion
    return simulated_annealing(lista,individuo,False)

@hug.get()
def seleccion(poblacion,n_poblacion,all_PL): #se seleccionan los k mejores (20%)
    for individuo in poblacion:              #para cada indivuduo de la poblacion calcula el fitness como la suma de los temple de todas las listas
        f_total = 0                          #por individuo inicia en 0 y luego le sumamos lo acumulado
        for lista in all_PL:
            f_total += calcular_fitness(lista,individuo.genes) 
        individuo.fitness = f_total
    k = int(0.20*n_poblacion)                #nro de seleccionados
    if k%2 == 1:                             #para que los seleccionados sean pares
        k += 1
    seleccionados = []
    i = 0
    for m in range(k):
        seleccionados.append(Individuo())
    while i!=k:
        j = 0
        f_min = poblacion[j].fitness         #valor semilla
        while poblacion[j] in seleccionados: #corrige cuando el 1er elemento fue seleccionado->ya no sirve de semilla
            j += 1
            f_min = poblacion[j].fitness
            
        for individuo in poblacion:
            if individuo.fitness <= f_min and individuo not in seleccionados:
                f_min = individuo.fitness
                seleccionados[i] = individuo
        i += 1
    return seleccionados

@hug.get()
def crossover(seleccionados):               #Crossover por cruce de orden
    for i in range(0,len(seleccionados),2): #los seleccionados pares
        corte1 = rd.randint(1,46)           #1 y 46 aseguran q haya al menos un nro a cada lado
        corte2 = rd.randint(1,46)           #recordar que el ultimo indice es 47
        listaA = seleccionados[i].genes     #para tener un nombre mas corto
        listaB = seleccionados[i+1].genes
        while corte1 == corte2:             #por si se llegara a repetir
            corte2 = rd.randint(1,46)
        if corte1 > corte2:                 #para mantener que cruce 1 sea menor que cruce2
            corte1,corte2 = corte2,corte1
        newA = []
        newB = []
        for j in range(len(listaA)):
            newA.append(0)
            newB.append(0)

        for k in range(corte1,corte2+1):    #corte 2 inclusive, por esto el +1
            newA[k] = listaB[k]
            newB[k] = listaA[k]
        
        seleccionados[i].genes = cross_over_parte2(corte1,corte2,listaA,newA)
        seleccionados[i+1].genes = cross_over_parte2(corte1,corte2,listaB,newB)
    return seleccionados

def cross_over_parte2(corte1,corte2,lista,new_):
    it = corte2+1                       
    actual = it                         
    while actual != corte1: #se completa la lista llamada new desde corte2 hasta corte1
        if actual == len(lista):
            actual = 0
        num = lista[it]
        while num in new_:
            it += 1
            if it == len(lista):
                it = 0
            num = lista[it]
        new_[actual] = num
        actual += 1
    return new_

@hug.get()
def mutacion(seleccionados):
    for ind in seleccionados:
        probab_de_mutar = rd.random()
        if probab_de_mutar < 0.15:
            gen1 = rd.randint(0,47)
            gen2 = rd.randint(0,47)
            while gen1 == gen2:         #por si se llegara a repetir
                gen2 = rd.randint(0,47)
            ind.genes[gen1],ind.genes[gen2] = ind.genes[gen2],ind.genes[gen1]
    return seleccionados

@hug.get()
def buscar_el_mejor(poblacion):
    fitness_min = poblacion[0].fitness #semilla de fitness
    mejor = poblacion[0]               #semilla de individuo
    for individuo in poblacion:
        if individuo.fitness < fitness_min:
            fitness_min = individuo.fitness
            mejor = individuo
    return mejor

@hug.get()
def algoritmo_genetico():
    all_PL = crear_lista_picking() #3)
    n_poblacion = 40 #<-- <-- <-- <-- <-- <--TAMANO DE POBLACION
    poblacion = generar_primer_poblacion(n_poblacion) 
    
    generacion = 0
    max_generacion = 50

    while(generacion < max_generacion): #criterio de parada: tiempo transcurrido
        seleccionados = seleccion(poblacion,n_poblacion,all_PL)
        seleccionados = crossover(seleccionados)
        seleccionados = mutacion(seleccionados)
        generacion += 1
    
    mejor_ind = buscar_el_mejor(poblacion)
    map = generate_map(mejor_ind.genes)
    print("\nEl mejor individuo de la poblacion es:\n",mejor_ind.genes,"\n\n",map)

