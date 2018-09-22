"""
Author: D Jayme Green
Date: 4/9/17
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
#euclideanDist = [[]]
#rowsWithClassifier = 0




"""
Reading in the .csv file and putting it into listOfData which
holds all of the columns as lists. It relies on the file to have
a header on the top
"""
def openCSVFile(fileName):
    listOfData = list()
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        totalNumOfCars = 0
        colNum = len(next(reader))
        nonNumbers = 0
        for col in range(0,colNum):
            listOfData.append(list())
        for row in reader:
            for val in range(0,colNum):
                try:
                    listOfData[val].append(float(row[val]))
                except ValueError:
                    nonNumbers += 1
            totalNumOfCars += 1
    return listOfData

listOfData = openCSVFile('d1LaxRankings.csv')

"""
Finds the Mean of the given column
"""
def findMean(col):
    sum = 0
    for value in listOfData[col]:
        sum += value
    return (float(sum)/len(listOfData[col]))


"""
Find the standard deviation of the given column
"""
def findStandardDeviation(col):
    mean = findMean(col)
    summation = 0
    for num in listOfData[col]:
        summation += pow((num - mean),2)
    variance = float(summation)/(float(len(listOfData[col])-1))
    return (math.sqrt(variance))

"""
Does the Cross Correlation of the two parameters
"""
def crossCorrelate(interestedCol, targetCol):
    beginMultiply = 1.0/float(len(listOfData[targetCol])-1)
    inside = 0
    interestedMean = findMean(interestedCol)
    interestedSD = findStandardDeviation(interestedCol)
    targetMean = findMean(targetCol)
    targetSD = findStandardDeviation(targetCol)
    for row in range(0,len(listOfData[targetCol])):
        interested = float(listOfData[interestedCol][row] - interestedMean)/float(interestedSD)
        target = float(listOfData[targetCol][row] - targetMean)/float(targetSD)
        inside += interested * target
    return (inside * beginMultiply)

"""
Does the Cross Correlation analysis for every attribute 
"""
def findAllCrossCorrelations():
    targetCol = len(listOfData)-1
    targetColName = "Winning Percentage"
    colNames = ['Teams','Goals','Goals Allowed','Faceoff Win','Manup Goal','Mandown Goal', 'Scoring Margin', 'Penalties', 'Turnovers', 'Caused Turnovers', 'Shot Percentage', 'GB', 'Assists', 'Saves', 'Clearing', 'Points', 'Winning Percentage']

    for attribute in range(1,len(listOfData)-2):
        print("Cross Correlation of " + colNames[attribute] + " and " + targetColName + ": " + str(crossCorrelate(attribute, targetCol)))


findAllCrossCorrelations()