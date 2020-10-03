#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams['image.cmap'] = 'gray'
from mpl_toolkits.mplot3d import Axes3D
from skimage import color, img_as_float
import cv2
import mahotas
import pandas as pd

#Crear API REST con Hug
import hug

@hug.get()
def extraccion(parametro):
    #Humedad del suelo
    humedad = parametro[0]
    #Velocidad del viento
    viento = parametro[1]
    #Cercania a fuentes de Agua
    nearWater = parametro[2]
    
    return parametro, [humedad, viento, nearWater]

#Analisis de la base de datos (Train)
##Entrenamiento de la base de datos 
extremo =   #pd.read_csv(PATH_FILE_extremo.csv)
alto =      #pd.read_csv(PATH__FILE_alto.csv)
moderado =  #pd.read_csv(PATH__FILE_moderado.csv)
bajo =      #pd.read_csv(PATH__FILE_bajo.csv)
        
#Elemento de analisis estadistico
class Elemento:
    def __init__(self):
        self.clasePeligro = None
        self.parametro = None
        self.caracteristica = []
        self.distancia = 0
        
#Analisis de datos
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

datos = []
i = 0

# Analisis de extremos
iter = 0
for objeto in extremo:
    datos.append(Elemento())
    datos[i].clasePeligro = 'Extremo'
    datos[i].parametro, datos[i].caracteristica = extraccion(objeto)
    ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='y', marker='o')
    i += 1
    iter += 1
print("extremos OK")

# Analisis de altos
iter = 0
for objeto in alto:
    datos.append(Elemento())
    datos[i].clasePeligro = 'alto'
    datos[i].parametro, datos[i].caracteristica = extraccion(objeto)
    ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='r', marker='o')
    i += 1
    iter += 1
print("altos OK")

# Analisis de moderados
iter = 0
for objeto in moderado:
    datos.append(Elemento())
    datos[i].clasePeligro = 'moderado'
    datos[i].parametro, datos[i].caracteristica = extraccion(objeto)
    ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='b', marker='o')
    i += 1
    iter += 1
print("moderados OK")

# Analisis de bajos
iter = 0
for objeto in bajo:
    datos.append(Elemento())
    datos[i].clasePeligro = 'bajo'
    datos[i].parametro, datos[i].caracteristica = extraccion(objeto)
    ax.scatter(datos[i].caracteristica[0], datos[i].caracteristica[1], datos[i].caracteristica[2], c='g', marker='o')
    i += 1
    iter += 1
print("bajos OK")

ax.grid(True)
ax.set_title("Analisis completo de Train")

yellow_patch = mpatches.Patch(color='yellow', label='extremo')
red_patch = mpatches.Patch(color='red', label='alto')
blue_patch = mpatches.Patch(color='blue', label='moderado')
green_patch = mpatches.Patch(color='green', label='bajo')
plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

ax.set_xlabel('Humedad')
ax.set_ylabel('Velocidad del viento')
ax.set_zlabel('Cercania a recurso hídricos')

plt.show()

print("Analisis completo de la base de datos de YTrain")
print("Cantidad de imagenes analizadas: ")
print(len(datos))

# Elemento a evaluar
#Recordar aplicar Transformacion.py cuando se quiera evaluar una nueva imagen.
test = Elemento()
parametro = input("Introduce el parametro a analizar: ")

test.parametro, test.caracteristica = extraccion(parametro)
test.clasePeligro = 'moderado' # label inicial 

ax.scatter(test.caracteristica[0], test.caracteristica[1], test.caracteristica[2], c='k', marker='o')
fig

#KNN
print("\nInicializacion KNN")
i = 0
sum = 0
for ft in datos[0].caracteristica:
        sum = sum + np.power(np.abs(test.caracteristica[i] - ft), 2)
        i += 1
d = np.sqrt(sum)

for element in datos:
    sum = 0
    i = 0
    for ft in (element.caracteristica):
        sum = sum + np.power(np.abs((test.caracteristica[i]) - ft), 2)
        i += 1
    
    element.distancia = np.sqrt(sum)
    
    if (sum < d):
        d = sum
        test.clasePeligro = element.clasePeligro

print("Prediccion para KNN con K=1: ")    
print(test.clasePeligro)

# Algoritmo de ordenamiento de BuvvleSort-> lo elegi porque es bastante estable
swap = True
while (swap):
    swap = False
    for i in range(1, len(datos)-1) :
        if (datos[i-1].distancia > datos[i].distancia):
            aux = datos[i]
            datos[i] = datos[i-1]
            datos[i-1] = aux
            swap = True
print("\nPredicciones para KNN con K=9: ")            
k = 9
for i in range(k):
    print(datos[i].clasePeligro)

#K MEANS
import random
print("\nInicializacion KMeans")

extremo_data = []
alto_data = []
moderado_data = []
bajo_data = []

for element in datos:
    if (element.clasePeligro == 'extremo'):
        extremo_data.append(element)
    if (element.clasePeligro == 'alto'):
        alto_data.append(element)
    if (element.clasePeligro == 'moderado'):
        moderado_data.append(element)
    if (element.clasePeligro == 'bajo'):
        bajo_data.append(element)

extremo_mean = list(random.choice(extremo_data).caracteristica)
alto_mean = list(random.choice(alto_data).caracteristica)
moderado_mean = list(random.choice(moderado_data).caracteristica)
bajo_mean = list(random.choice(bajo_data).caracteristica)


fig_means = plt.figure()
ax = fig_means.add_subplot(111, projection='3d')

# fig_means, ax = plt.subplots()
ax.scatter(extremo_mean[0], extremo_mean[1], extremo_mean[2], c='y', marker='o')
ax.scatter(alto_mean[0], alto_mean[1], alto_mean[2], c='r', marker='o')
ax.scatter(moderado_mean[0], moderado_mean[1], moderado_mean[2], c='b', marker='o')
ax.scatter(bajo_mean[0], bajo_mean[1], bajo_mean[2], c='g', marker='o')

ax.grid(True)
ax.set_title("Means")

yellow_patch = mpatches.Patch(color='yellow', label='extremo')
red_patch = mpatches.Patch(color='red', label='alto')
blue_patch = mpatches.Patch(color='blue', label='moderado')
green_patch = mpatches.Patch(color='green', label='bajo')
plt.legend(handles=[yellow_patch, red_patch, blue_patch, green_patch])

ax.set_xlabel('Humedad')
ax.set_ylabel('Velocidad del viento')
ax.set_zlabel('Cercania a recurso hídricos')

plt.show()

# Asignacion, Actualizacion y Convergencia
extremo_flag = True
alto_flag = True
moderado_flag = True
bajo_flag = True

extremo_len = [0, 0, 0]
alto_len = [0, 0, 0]
moderado_len = [0, 0, 0]
bajo_len = [0, 0, 0]

iter = 0
while (iter < 20):

    extremo_data = []
    alto_data = []
    moderado_data = []
    bajo_data = []

    # ASIGNACION
    for element in datos:
        sum_extremo = 0
        sum_alto = 0
        sum_moderado = 0
        sum_bajo = 0

        for i in range(0, len(element.caracteristica)-1):
            sum_extremo += np.power(np.abs(extremo_mean[i] - element.caracteristica[i]), 2)
            sum_alto += np.power(np.abs(alto_mean[i] - element.caracteristica[i]), 2)
            sum_moderado += np.power(np.abs(moderado_mean[i] - element.caracteristica[i]), 2)
            sum_bajo += np.power(np.abs(bajo_mean[i] - element.caracteristica[i]), 2)

        dist_extremo = np.sqrt(sum_extremo)
        dist_alto = np.sqrt(sum_alto)
        dist_moderado = np.sqrt(sum_moderado)
        dist_bajo = np.sqrt(sum_bajo)
        
        aux = dist_extremo
        if (dist_alto < aux):
            aux = dist_alto
        if (dist_moderado < aux):
            aux = dist_moderado
        if (dist_bajo < aux):
            aux = dist_bajo
            
        if (aux == dist_extremo):
            extremo_data.append(element.caracteristica)
        elif (aux == dist_alto):
            alto_data.append(element.caracteristica)
        elif(aux == dist_moderado):
            moderado_data.append(element.caracteristica)
        elif(aux == dist_bajo):
            bajo_data.append(element.caracteristica)
            
    # ACTUALIZACION
    sum_extremo = [0, 0, 0]
    for b in extremo_data:
        sum_extremo[0] += b[0]
        sum_extremo[1] += b[1]
        sum_extremo[2] += b[2]

    sum_alto = [0, 0, 0]
    for o in alto_data:
        sum_alto[0] += o[0]
        sum_alto[1] += o[1]
        sum_alto[2] += o[2]

    sum_moderado = [0, 0, 0]
    for l in moderado_data:
        sum_moderado[0] += l[0]
        sum_moderado[1] += l[1]
        sum_moderado[2] += l[2]

    sum_bajo = [0, 0, 0]
    for p in bajo_data:
        sum_bajo[0] += p[0]
        sum_bajo[1] += p[1]
        sum_bajo[2] += p[2]
        
    extremo_mean[0] = sum_extremo[0] / len(extremo_data)
    extremo_mean[1] = sum_extremo[1] / len(extremo_data)
    extremo_mean[2] = sum_extremo[2] / len(extremo_data)

    alto_mean[0] = sum_alto[0] / len(alto_data)
    alto_mean[1] = sum_alto[1] / len(alto_data)
    alto_mean[2] = sum_alto[2] / len(alto_data)

    moderado_mean[0] = sum_moderado[0] / len(moderado_data)
    moderado_mean[1] = sum_moderado[1] / len(moderado_data)
    moderado_mean[2] = sum_moderado[1] / len(moderado_data)
    
    bajo_mean[0] = sum_bajo[0] / len(bajo_data)
    bajo_mean[1] = sum_bajo[1] / len(bajo_data)
    bajo_mean[2] = sum_bajo[1] / len(bajo_data)
    
    #print("extremo  alto  moderado  bajo")
    #print(len(extremo_data), len(alto_data), len(moderado_data), len(bajo_data))
    
    # CONVERGENCIA Y CONDICION DE SALIDA
    
    if (extremo_mean == extremo_len):
        extremo_flag = False
    else:
        extremo_len = extremo_mean

    if (alto_mean == alto_len):
        alto_flag = False
    else:
        alto_len = alto_mean

    if (moderado_mean == moderado_len):
        moderado_flag = False
    else:
        moderado_len = moderado_mean
            
    if (bajo_mean == bajo_len):
        bajo_flag = False
    else:
        bajo_len = bajo_mean

    iter += 1
    
# Ubicacion de los means finales
ax.scatter(extremo_mean[0], extremo_mean[1], extremo_mean[2], c='k', marker='o')
ax.scatter(alto_mean[0], alto_mean[1], alto_mean[2], c='k', marker='o')
ax.scatter(moderado_mean[0], moderado_mean[1], moderado_mean[2], c='k', marker='o')
ax.scatter(bajo_mean[0], bajo_mean[1], bajo_mean[2], c='k', marker='o')

print("Ubicacion de los means finales")
print("extremo  alto  moderado  bajo")
print(len(extremo_data), len(alto_data), len(moderado_data), len(bajo_data))
fig_means

##Mean mas cercano
sum_extremo = 0
sum_alto = 0
sum_moderado = 0
sum_bajo = 0

for i in range(0, len(test.caracteristica)-1):
    sum_extremo += np.power(np.abs(test.caracteristica[i] - extremo_mean[i]), 2)
    sum_alto += np.power(np.abs(test.caracteristica[i] - alto_mean[i]), 2)
    sum_moderado += np.power(np.abs(test.caracteristica[i] - moderado_mean[i]), 2)
    sum_bajo += np.power(np.abs(test.caracteristica[i] - bajo_mean[i]), 2)

dist_extremo = np.sqrt(sum_extremo)
dist_alto = np.sqrt(sum_alto)
dist_moderado = np.sqrt(sum_moderado)
dist_bajo = np.sqrt(sum_bajo)

print("\nMean mas cercano")
print("extremo  alto  moderado  bajo")
print(dist_extremo, dist_alto, dist_moderado, dist_bajo)

aux = dist_extremo
if (dist_alto < aux):
    aux = dist_alto
if (dist_moderado < aux):
    aux = dist_moderado
if (dist_bajo < aux):
    aux = dist_bajo

if (aux == dist_extremo):
    test.clasePeligro = 'extremo'
elif (aux == dist_alto):
    test.clasePeligro = 'alto'
elif(aux == dist_moderado):
    test.clasePeligro = 'moderado'
elif(aux == dist_bajo):
    test.clasePeligro = 'bajo'

print("\nPrediccion para KMeans: ")
print(test.clasePeligro) 
