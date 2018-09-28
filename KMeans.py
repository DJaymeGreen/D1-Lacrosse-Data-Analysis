"""
Author: D Jayme Green
Date: 9/27/2018
K-Means


This program creates a clusters using the given 
Testing data
"""

"""
Csv is used to read in the csv data
Numpy is used to allow floats into Matplotlib
"""
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import csv
import math
import numpy as np
import sys
import random


"""
Constants are declared below for the program
listOfData holds all of the data given
totalNumberOfVals holds the number of rows there is
numberOfCols holds the number of cols there is
"""
listOfData = list(list())
totalNumberOfVals = 0
numberOfCols = 0
whatCluster = dict()
clusters = list(list())
combinedRows = list()
whatTeam = dict()
#euclideanDist = [[]]
#rowsWithClassifier = 0




"""
Reading in the .csv file and putting it into listOfData which
holds all of the rows as lists. It relies on the file to have
a header on the top
"""
def openCSVFile(fileName):
    listOfData = list()
    teamRow = dict()
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        rowNum = 0
        colNum = len(next(reader))
        #for col in range(0,colNum-1):
         #   listOfData.append(list())
        skipRows = set()
        for row in reader:
            listOfData.append(list())
            teamRow[rowNum] = row[0]
            for val in range(1,colNum):
                try:
                    listOfData[rowNum].append(float(row[val]))
                except ValueError:
                    listOfData[rowNum].append(row[val])
                    skipRows.add(rowNum)
            rowNum += 1

        # Delete the rows where there is a String
        skipRows = sorted(skipRows)
        for rowRemove in reversed(skipRows):
            listOfData.pop(rowRemove)

    return listOfData, rowNum, colNum, teamRow

listOfData, totalNumberOfVals, numberOfCols, whatTeam = openCSVFile('d1LaxRankings.csv')

"""
Finds the mininum and maximum value of the attribute (column) given
@param      attributeIndex          The attribute number to return
@return     Min, Max                The minimum value in the column
                                    The maximum value in the column
"""
def findMinMaxVals(attributeIndex):
    minVal = sys.float_info.max
    maxVal = -sys.float_info.max
    for row in listOfData:
        if row[attributeIndex] < minVal:
            minVal = row[attributeIndex]
        if row[attributeIndex] > maxVal:
            maxVal = row[attributeIndex]
    return minVal,maxVal

"""
Creates the whatPoint dictionary. This contains all of the points and what
center point that the row is clustered to.
The key: The row
The Value: What point/cluster it is associated with
"""
def createWhatPoint():
    whatPoint = dict()
    for row in range(0, len(listOfData)):
        whatPoint[row] = [row]
    return whatPoint

"""
Creates the original list of center points
@param      k       The amount of center points (clusters) to have
"""
def createListOfCenters(k):
    centers = [[] for numberOfK in range(k)]
    minMaxVals = list()
    for attribute in range(0,len(listOfData[0])):
        minMaxVals.append(findMinMaxVals(attribute))
        #centers[attribute] = list()
    for kRandomStarts in range(0,k):
        for attribute in range(0,len(listOfData[0])):
            centers[kRandomStarts].append((random.randint(int(minMaxVals[attribute][0]),int(minMaxVals[attribute][1]))))
    return centers

"""
Function that tests createListOfCenters and createWhatPoints
"""
def testCenters():
    centers = createListOfCenters(3)
    whatPoint = createWhatPoint();
    centers = createListOfCenters(5)
    whatPoint = createWhatPoint()
    centers = createListOfCenters(10)
    whatPoint = createWhatPoint()

#Yay it works!
#testCenters()

"""
Finds the closes center point of all the points using the Euclidean distance 
@param      whatPoint       All of the points
@param      center          The center to find the euclidean distance to
"""
def findAndSetEuclideanClosesCenter(whatPoint, center):
    
    #rowOneIndex = findClusterWithID(rowOne)
    #rowTwoIndex = findClusterWithID(rowTwo)
    for point in whatPoint.keys():
        bestDistance = sys.float_info.max
        bestCenter = 0
        for centers in range(0, len(center)):
            distance = 0
            for attributeOfRow in range(0, len(center[0])):
                distance += pow(center[centers][attributeOfRow] - listOfData[point][attributeOfRow], 2)
            distance = math.sqrt(distance)
            if(distance < bestDistance):
                bestDistance = distance
                bestCenter = centers
        whatPoint[point] = bestCenter
    return whatPoint
    
"""
Finds and sets the new center points based on the Center of Mass of 
the points assigned to them
@param          whatPoint           Dictionary containing the points and what
                                    center they are associated with
@param          center              All of the centers
@return                             The new centers
"""
def findAndSetNewCenters(whatPoint, center):
    centers = [[0 for numOfAttributes in range(len(listOfData[0]))] for numberOfClusters in range(len(center))]
    centerTotalPoints = [0 for defaultZero in range(len(center))]
    for point in whatPoint.keys():
        for dimension in range(0,len(listOfData[0])):
            temp = listOfData[point][dimension]
            centers[whatPoint.get(point)][dimension] += temp
        centerTotalPoints[whatPoint[point]] +=1
    for center in range(0,len(centers)):
        for dim in range(0, len(centers[0])):
            centers[center][dim] /= (centerTotalPoints[center] if centerTotalPoints[center] != 0  else 1)
    return centers

"""
Finds the Sum of Squared Error (SSE) of the given clusters
@param          whatPoint           Dictionary containing the points and what 
                                    center they are associated with
@param          center              All of the centers
@return         SSE                 The Sum of Squared Error of the clusters
"""
def findSSE(whatPoint, center):
    sse = 0
    for kClusters in range(0,len(center)):
        for pointsInClusters in range(0,len(whatPoint.keys())):
            if(whatPoint[pointsInClusters] == kClusters):
                sse += math.pow(findEuclideanDistance(pointsInClusters,center[kClusters]),2)
    return sse

"""
Finds the Euclidean Distance between the point and the center given
@param          point               The point/row of the point to find the
                                    Euclidean Distance of
@param          center              The center points to find the Euclidean Distance of
@return                             The Euclidean Distance
"""
def findEuclideanDistance(point,center):
    sse = 0
    for attributes in range(0,len(center)):
        sse += math.pow(listOfData[point][attributes] - center[attributes],2)
    return(math.sqrt(sse))

"""
Graphs k vs see
"""
def graphSSEvsK(allK, allSSE):
    mpl.plot(allK,allSSE,'ro')
    mpl.xlabel("K")
    mpl.ylabel("Error")
    mpl.title("K vs SSE")
    mpl.show()

"""
Does K-means a few times to find the best K value by using different K values
"""
def findBestK(whatPoint):
    allK = list()
    allSSE = list()
    bestK = 0
    bestSSE = sys.float_info.max
    sse = 0
    ssePrev = sys.float_info.max
    lastBestSSE = sys.float_info.max
    for kClusters in range(2,len(listOfData)//10):
        centers = createListOfCenters(kClusters)
        numberOfIterations = 0
        ssePrev = sys.float_info.max
        sse = 0
        while((math.fabs(ssePrev-sse) > 0.1) and numberOfIterations < 25):
            whatPoint = findAndSetEuclideanClosesCenter(whatPoint,centers)
            centers = findAndSetNewCenters(whatPoint,centers)
            ssePrev = sse
            sse = findSSE(whatPoint,centers)
            numberOfIterations += 1
        allK.append(kClusters)
        allSSE.append(sse)
        if(bestSSE > sse):
            if(bestSSE != sys.float_info.max):
                lastBestSSE = bestSSE
            bestK = kClusters
            bestSSE = sse
        if((bestSSE/lastBestSSE) > 0.7):
            break
        print("( " + str(kClusters) + ", " + str(sse) + ")");

    #Get the last point for the graph, we already found bestK
    centers = createListOfCenters(bestK+1)
    lastBestSSE = sys.float_info.max
    numberOfIterations = 0
    while(numberOfIterations < 25):
        whatPoint = findAndSetEuclideanClosesCenter(whatPoint,centers)
        centers = findAndSetNewCenters(whatPoint,centers)
        sse = findSSE(whatPoint,centers)
        numberOfIterations += 1
        if (lastBestSSE > sse):
            lastBestSSE = sse
    
    allK.append(bestK+1)
    allSSE.append(lastBestSSE)

    graphSSEvsK(allK,allSSE)
    return bestK

#findBestK(createWhatPoint())

"""
Graphs the clusters
@param      whatPoint       Every point and what cluster they are associated with
"""
def graphClusters(whatPoint):
    x0 = list()
    y0 = list()
    z0 = list()

    x1 = list()
    y1 = list()
    z1 = list()

    x2 = list()
    y2 = list()
    z2 = list()

    x3 = list()
    y3 = list()
    z3 = list()

    fig = mpl.figure()
    ax = fig.add_subplot(111,projection='3d')

    for point in whatPoint.keys():
        if (whatPoint[point] == 0):
            x0.append(listOfData[point][0])
            y0.append(listOfData[point][1])
            z0.append(listOfData[point][2])
        elif (whatPoint[point] == 1):
            x1.append(listOfData[point][0])
            y1.append(listOfData[point][1])
            z1.append(listOfData[point][2])
        elif (whatPoint[point] == 2):
            x2.append(listOfData[point][0])
            y2.append(listOfData[point][1])
            z2.append(listOfData[point][2])
        elif (whatPoint[point] == 3):
            x3.append(listOfData[point][0])
            y3.append(listOfData[point][1])
            z3.append(listOfData[point][2])

    print("Cluster 1")
    print(len(x0))
    for point in range(0,len(x0)):
        print("(" + str(x0[point]) + "," + str(y0[point]) + "," + str(z0[point]) + ")")
    print("Cluster 2")
    print(len(x1))
    for point in range(0,len(x1)):
        print("(" + str(x1[point]) + "," + str(y1[point]) + "," + str(z1[point]) + ")")
    print("Cluster 3")
    print(len(x2))
    for point in range(0,len(x2)):
        print("(" + str(x2[point]) + "," + str(y2[point]) + "," + str(z2[point]) + ")")
    print("Cluster 4")
    print(len(x3))
    for point in range(0,len(x3)):
        print("(" + str(x3[point]) + "," + str(y3[point]) + "," + str(z3[point]) + ")")

    ax.scatter(x0,y0,z0,c='red')
    ax.scatter(x1,y1,z1,c='green')
    ax.scatter(x2,y2,z2,c='blue')
    ax.scatter(x3,y3,z3,c='yellow')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    mpl.show()

"""
Does the generic K Means algorithm. 
"""
def genericKMeans():
    whatPoint = createWhatPoint()
    k = findBestK(whatPoint)
    bestSSE = sys.float_info.max
    
    # For some number of iterations
    for kMeansIterations in range(0, 200):
        #Select initial seed points as prototype centers (at random) for the clusters:
        centers = createListOfCenters(k)
        ssePrev = sys.float_info.max
        sse = 0
        #Repeat:
        # Stop whent he prototypes do not move
        while((math.fabs(ssePrev-sse) > 0.1)):
            #Assign all data points to the closest center
            whatPoint = findAndSetEuclideanClosesCenter(whatPoint,centers)
            # For each cluster formed, find the new prototype center for the center
            centers = findAndSetNewCenters(whatPoint,centers)
            ssePrev = sse
            sse = findSSE(whatPoint,centers)
        #Evaluate the resulting clustering (using SSE) for each iteration, save the best
        if(bestSSE > sse):
            bestSSE = sse
            bestCenters = centers
            bestWhatPoint = whatPoint
    
    # Use the best set of prototypes
    return (bestSSE, bestCenters, bestWhatPoint)


"""
Calls the function that does the KMeans and prints out the points and what
cluster they belong to
"""
def printKMeansCluster():
    bestSSE, bestCenters, bestWhatPoint = genericKMeans()
    print("The best SSE: " + str(bestSSE))
    for point in bestWhatPoint.keys():
        print(str(whatTeam[point]) + " center: " + str(bestWhatPoint.get(point)))
    #graphClusters(bestWhatPoint)

printKMeansCluster()

    
   
    
    



