#!/usr/bin/env python
# coding: utf-8

# In[11]:


#Chargement des librairies utiles
import pandas as pd #Pour la lecture des données
import numpy as np #Pour les opérations mathématiques
pd.set_option('display.max_rows', 500)
pd.set_option('max_colwidth', None)


# In[12]:


#Chargement des data dans deux dataframes df et df1
xls = pd.ExcelFile('/Users/aliwalid/Desktop/Projet CL03/cl03-projet-1-data.xlsx')
df = pd.read_excel(xls, 'NODES')
df = df.where(pd.notnull(df), '-')
df1 = pd.read_excel(xls, 'EDGES')
df


# In[13]:


#Fonction permettant de calculer B(i,t)
def B(x1, x2, y1, y2):
    x = (x2 - x1)**2
    y = (y2 - y1)**2
    return (np.sqrt(x + y))/1000


# In[14]:


#Construction de la matrice d'adjacence
graph = np.zeros((287,287),dtype = float) #Initialisation d'une matrice de 0
nb_arete = len(df1)
for i in range(nb_arete):                 #Remplissage avec lecture des dataframes
    noeud1 = df1['NOEUD_1'][i]
    noeud2 = df1['NOEUD_2'][i]
    longueur = df1['LONGUEUR'][i]  
    graph[noeud1-1][noeud2-1] = longueur
    graph[noeud2-1][noeud1-1] = longueur  #Ne pas oublier qu'on a des arêtes -> matrice symétrique


# In[76]:


#Fonction permettant d'appliquer l'algorithme de Dijkstra sur un noeud de départ et un noeud d'arrivée
def dijkstra(graph, start, end):
    start = start - 1 
    end = end - 1
    
    visitedNodes = []
    nbNodes = len(graph)
    inf = sum(sum(line) for line in graph) + 1
    total = 0
    
    allNodes = []
    distanceMin = []
    paths = []
    for i in range(nbNodes):
        allNodes.append(i)
        distanceMin.append(inf)
        paths.append([])
    
    distanceMin[start] = 0

    while len(visitedNodes) < nbNodes:
        
        notVisitedNodes = np.setdiff1d(allNodes, visitedNodes)
        notVisitedDistances = []
        for i in range(nbNodes):
             notVisitedDistances.append(inf)
        for node in notVisitedNodes:
            notVisitedDistances[node] = distanceMin[node]
        
        currentNode = notVisitedDistances.index(min(notVisitedDistances))
        currentPath = paths[currentNode]
        total = total + 1
        
        visitedNodes.append(currentNode)
        
        if currentNode == end:
            break

        successors = []
        for j, v in enumerate(graph[currentNode]):
            if v != 0:
                successors.append(j)
        
        for successor in successors:
            distance = distanceMin[currentNode] + graph[currentNode][successor]
            if distance < distanceMin[successor]:
                distanceMin[successor] = distance
                paths[successor] = currentPath + [currentNode + 1]
      
    return { 'path': paths[end] + [end + 1], 'fixedNodes': total, 'distance': distanceMin[end] }


# In[77]:


dijkstra(graph, 239, 14)


# In[72]:


#Fonction permettant d'appliquer l'algorithme de Sedgewick-Vitter sur un noeud de départ et un noeud d'arrivée
def sedgewickVitter(graph, start, end, df):
    
    start = start - 1
    end = end - 1
    
    visitedNodes = []
    nbNodes = len(graph)
    inf = sum(sum(line) for line in graph) + 1
    total = 0
    
    allNodes = []
    distanceMin = []
    paths = []
    
    for i in range(nbNodes):
        allNodes.append(i)
        distanceMin.append(inf)
        paths.append([])
    
    distanceMin[start] = 0
    coordEnd =  {'x': df['X'][end], 'y': df['Y'][end] }
    
    while len(visitedNodes) < nbNodes:
        notVisitedNodes = np.setdiff1d(allNodes, visitedNodes)
        notVisitedDistances = [] 
        for i in range(nbNodes):
             notVisitedDistances.append(inf)
        
        for node in notVisitedNodes:
            coordNode =  {'x': df['X'][node], 'y': df['Y'][node] } #Calcul des coordonnées du current node
            borne = B(coordNode['x'],coordEnd['x'] ,coordNode['y'], coordEnd['y']) #calcul de b(i,t)
            notVisitedDistances[node] = distanceMin[node] + borne 
            
        currentNode = notVisitedDistances.index(min(notVisitedDistances))
        currentPath = paths[currentNode]
        total = total + 1
        
        visitedNodes.append(currentNode)
        
        if currentNode == end:
            break

        successors = [] 
        for j, v in enumerate(graph[currentNode]):
            if v != 0:
                successors.append(j)
        
        for successor in successors:
            distance = distanceMin[currentNode] + graph[currentNode][successor]
            
            if distance < distanceMin[successor]:
                distanceMin[successor] = distance
                paths[successor] = currentPath + [currentNode + 1]
      
    return { 'path': paths[end] + [end + 1], 'fixedNodes': total, 'distance': distanceMin[end] }


# In[78]:


sedgewickVitter(graph, 239, 14, df)

