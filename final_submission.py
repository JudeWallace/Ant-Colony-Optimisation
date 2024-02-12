"""
This module contains a collection of functions performing the elitist ACO
algorithm on the TSP problem, contained in XML files burma14 and brazil58

Functions:
    - xml_decoder : Converts the XML to a numpy matrix representing the weighted graph
    - calculate_heuristic : Returns a matrix with heuristic weightings
    - calculate_path_cost : Returns the cost for each path completed by an ant
    - update_pheremone : Updates the pheremones on the path edges
    - ant_colony_optimisation : Main logic for ACO

Author: Jude Wallace
    Date: December 10, 2023
"""

# Imports
import xml.etree.cElementTree as ET
import numpy as np
import random

# Global constant variables:
RHO = 0.5 # evaporation rate
Q = 5 # local heuristic variable
ALPHA =  1 #local search bias
BETA = 3 # global search bias
K = 50 # number of ants in the colony
ITER = 200 # number of iterations
ELITIST = False # Boolean to set if Elitist ACO is desired
ELITISTFACTOR = 0.20 # % of ants to be elitist (0.1 = 10% etc)

def xml_decoder(filename):
    """
    Converts the XML file to a graph stored in an array
    
    Args:
        filename : Path to the XML file

    Returns:
        adjMatrix : A numpy matrix representation of the graph
        numVertices : The number of nodes in the graph
    """
    
    XMLtree = ET.parse(filename)

    myroot = XMLtree.getroot()

    # Find the number of vertices
    nodes = len(myroot.find('.//graph/vertex')) + 1

    # Create an empty adjacency matrix
    edges = np.zeros((nodes, nodes))

    # Fill the adjacency matrix
    sourceVertexID = 1
    for vertex in myroot.find('.//graph'):
        
        for edge in vertex.findall('edge'):
            targetvVertexID = int(edge.text)
            cost = float(edge.get('cost'))
            edges[sourceVertexID - 1, targetvVertexID] = cost
            
        sourceVertexID += 1

    return edges.astype(int), nodes

def calculate_heuristic(d, numVerticies):
    """
    Creates a simple heuristic matrix

    Args:
        d : distance matrix of the graph
        numVerticies : number of nodes in the grahh

    Returns:
       heuristicMatrix : The matrix with heuristic values
    """
    
    heuristicMatrix = np.ones((numVertices, numVertices))

    for i in range(numVertices):
        for j in range(numVertices):
            if i != j:
                heuristicMatrix[i][j] = round(Q / d[i][j], 4)
            else:
                heuristicMatrix[i][j] = 0

    return heuristicMatrix

def calculate_path_cost(matrix, path):
    """
    Calcuate the cost of the path the ant has taken

    Args:
        matrix : the cost matrix of the graph
        path : the path in i j format the ant took

    Returns:
        Total cost of the path from i back to i
    """
    
    # Extract the current and next nodes in the path
    currentNodes = path[:-1]
    nextNodes = path[1:]

    # Calculate the total cost
    totalCost = np.sum(matrix[currentNodes, nextNodes])

    return int(totalCost)

def update_pheremone(T, allPaths, pathCosts, numVertices, elitistIndex=[]):
    """
    Evaporate the current pheremones and deposit the new pheremones based on
    the ants path and path quality

    Args:
        T : pheremone matrix
        allPaths : 2D array of all paths taken in the iteration
        pathCosts : The cost of each path taken 
        elitistIndex : The index for which ant are elitist so their paths can 
                        recieve more pheremone
    """
    
    # evaportate and update the phemone T
    evaporationRate = (1 - RHO) * T
    T[:] = evaporationRate
    
    # Depsoit the necessary amount of pheremones on the edges i to j
    for i in range(len(allPaths)):
        path = allPaths[i]
        delta = 1/pathCosts[i]
            
        for j in range(numVertices - 1):
            T[path[j]][path[j+1]] += delta
            # Add addtional pheremone if elitist ants on
            if i in elitistIndex and ELITIST:
                 T[path[j]][path[j+1]] += pathCosts[i] * ELITISTFACTOR 

def ant_colony_optimisation(H1, numVertices):
    """
    Main logic of the ACO algorithm

    Args:
        H1 : The simple Heuristic matrix
        numVertices : number of nodes in the graph

    Returns:
       bestPathCost 
       bestPath
       worsePathCost
       worstPath
       avg : _description_
    """
    
    bestPathCost = 1000000000
    worsePathCost = 10
    worstPath = []
    bestPath = []
    avg = 0
    
    #Loop for iterations of the algorithm
    for x in range(ITER):
        
        #Store all iterations paths
        allPaths = []
        
        #Loop for how many ants in the colony
        for i in range(K):
            # Copy the heuristic so each ant has the information
            H = H1.copy()
            
            #Randomly select a city for starting node
            startingCity = random.randint(0, (numVertices - 1))

            # local path storage
            path = []
            
            #add starting city to path
            path.append(startingCity)
            
            #store current city ant is in
            curr = startingCity
            
            while len(path) != numVertices:
                
                # Remove all visited nodes from the probability heuristic
                H[:, path] = 0
                            
                # Transition formula for moving from i to j
    
                N = (T[curr] ** ALPHA) * (H[curr] ** BETA)

                den = np.sum(N)

                # Adding a small value to negate the div by 0 error potential
                P = N / den
                
                # Generate a random number [0,1] 
                rand = random.random()
                
                # Calcuate where the random value falls within the cities distribution
                CP = 0
                for i in range(numVertices):
                    CP += P[i]
                    if CP >= rand:
                        # Ant is to be in this city
                        curr = i
                        path.append(i)
                        break

            # Add the starting city to complete cycle
            path.append(startingCity)
            allPaths.append(path)
            
        # List of all the cost of the paths found in the iteration
        pathCosts = [calculate_path_cost(d, path) for path in allPaths]
        avg += sum(pathCosts)
        
        # Elitist ants selected
        if ELITIST:
            value = round(ELITISTFACTOR * K)
            elitistIndex = sorted(range(len(pathCosts)), key=lambda i: pathCosts[i], reverse=False)[:int(value)]
            update_pheremone(T, allPaths, pathCosts, numVertices, elitistIndex)
        else:
            # Update and evaporate pheremones
            update_pheremone(T, allPaths, pathCosts, numVertices)

        # Sort the paths into best to worst 
        pairs = list(zip(pathCosts, allPaths))
        
        sorted_pairs = sorted(pairs, key=lambda x: x[0])

        bCost = sorted_pairs[0][0]
        bPath = sorted_pairs[0][1]
        
        if bCost < bestPathCost:
            bestPathCost = bCost
            bestPath = bPath
        
        wCost = sorted_pairs[-1][0]
        wPath = sorted_pairs[-1][1]
        
        if wCost > worsePathCost:
            worsePathCost = wCost
            worstPath = wPath
            
    
    return bestPathCost, bestPath, worsePathCost, worstPath, round(avg / K * ITER)
                                                  
if __name__ == "__main__":
    # Decode XML TSP files
    burma = "burma14.xml"
    brazil = "brazil58.xml"
    d, numVertices = xml_decoder(brazil)
    
    # Calcualte Heuristic
    H1 = calculate_heuristic(d, numVertices)

    # Initalise pheremones randomly
    T = np.round(np.random.rand(numVertices, numVertices), 4)
    np.fill_diagonal(T, 0.0)
    
    print("Running simulation...")
    bestPathCost, bestPath, worsePathCost, worstPath, avg = ant_colony_optimisation(H1, numVertices)
    
    print(f"Best path found : {bestPathCost}, {bestPath}")
    