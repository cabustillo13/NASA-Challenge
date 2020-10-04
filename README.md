# NASA-Challenge

<p align="center">
 <img width="100px" src="https://github.com/cabustillo13/NASA-Challenge/blob/main/Nasa.svg" align="center" alt="NASA Space App Challenge" />
 <h2 align="center">NASA Space App Challenge 2020 in Mendoza, Argentina</h2>
 <p align="center"><b>Nosotros 1 - Fuego 0</b></p>
</p>

# Files
You can run this code in Python 2.7 and Python 3.x

```
___ Mapa
 |___ AEstrella.py            -> Pathfinder Algorithm
 |___ AlgoritmoGenetico.py    -> Genetic Algorithm
 |___ TempleSimulado.py       -> Annealing Algorithm
``` 
Input: A list with the order of the sources of where the fires occur.  

It's an API. It contains a genetic algorithm that allows you to order the order in which the fire sources should be turned off. It uses a simulated annealing algorithm for fitness. Which evaluates the distance between points with a Pathfinder algorithm. 

Output: Return an ordered list with which each source of fire must be extinguished.

```
___ Clasificacion
  |___ Main.py                -> KNN Algorithm and KMeans Algorithm
```
 
 Input: A parameter is passed that contains the data of: humidity, distance to the nearest water source and wind speed. This parameters are inside a csv file.
 
 It's an API. Historical humidity data, distance to the nearest water source and wind speed obtained from the SAOCOM satellite are read but you can use any source of information available in csv format. We use K-Nearest Neighbor(KNN) algorithm to classify the degree of fire (Extreme, high, medium and low) and KMeans algorithm to do a regression.
 
 Output: Determine degrees of fire (Extreme, high, medium and low).
