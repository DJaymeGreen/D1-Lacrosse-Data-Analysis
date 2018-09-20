"""
Author: D Jayme Green
Extracts the data from the csv given by the NCAA D1 Lacrosse
that I care about (the percentage and per game) that happen to be at
the end of the rows
"""

import csv

"""
Reading in the .csv file and putting it into listOfData which
has the team name and then the data that I want (happens to be 
at the end of each block of data). Each block has different width
provided by the NCAA
"""
def openCSVFile(fileName):
    listOfData = list()
    dictOfLaxTeamsList = dict()
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        rowNum = 0
        for row in reader:
            row = list(filter(None,row))
            colNum = len(row)
            if colNum > 1 and row[1] != 'Name':
                # Where the name is at col 1
                if row[1] not in dictOfLaxTeamsList:
                    dictOfLaxTeamsList[row[1]] = len(dictOfLaxTeamsList)
                    listOfData.append(list())
                    listOfData[dictOfLaxTeamsList[row[1]]].append(row[1])
                college = row[1]
                listOfData[dictOfLaxTeamsList[college]].append(float(row[colNum-1]))
            rowNum += 1
    return listOfData

"""
Writes all of the data into a new CSV file. Each team has a row
with each column being another piece of data
"""
def writeToCSV(listOfData):
    with open('d1LaxRankings.csv', 'w') as f:
        for team in listOfData:
            for stat in team:
                f.write(str(stat) + ',')
            f.write('\n')

listOfData, totalNumberOfVals, numberOfCols = openCSVFile('rankingsRaw.csv')
writeToCSV(listOfData)