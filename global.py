import sys
import numpy
import numpy as np


def getAlignment(tracebackGraph, sequences, matrix, edit):
    x = []
    y = []

    i = len(sequences[1]) #x
    j = len(sequences[0]) #y

    maxScore = edit[j][i]

    while (i > 0 or j > 0):

        current = tracebackGraph[j][i]
        if (current == 'DIAG'):
            y.append(sequences[0][j - 1])
            x.append(sequences[1][i - 1])
            i = i - 1
            j = j - 1
        elif (current == 'LEFT'):
            x.append(sequences[1][i - 1])
            y.append('-')
            i = i - 1
        elif (current == 'UP'):
            y.append(sequences[0][j - 1])
            x.append('-')
            j = j - 1
        else:
            break

    print(''.join(y[::-1]))
    print(''.join(x[::-1]))
    print(maxScore)

def match(element, matrix): #implement np where
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return (i,j)

def scoreTheMatch (char1, char2):
    row = match(char1, matrix)[1]
    column = match(char2, matrix)[1]
    return matrix[row][column]

def getEditGraph(sequences, matrix, gapPenalty):

    #creates a key value pairing that allows for us to access the matrix scoring value

    #matrixDictionary = {"A" : 3, "C" : 1, "G" : 4, "T" : 2}
    editGraph = []
    for i in range(len(sequences[0]) + 1):
        sub_matrix = [0]*(len(sequences[1]) + 1)
        editGraph.append(sub_matrix)# this will help us create a 2D array for the matrix to hold information from both sequences

    # here, we initialize the top row and left column with the gap values:
    for j in range(1, len(sequences[1]) + 1):
        editGraph[0][j] = j * gapPenalty

    for i in range(1, len(sequences[0]) + 1):
        editGraph[i][0] = i * gapPenalty


#     editGraph = [[0] * (len(sequences[0]) + 1) ] * (len(sequences[1]) + 1)

#why is it minus three???
    # for i in range(1, len(sequences[0]) - 3):
    #     editGraph[0][i] = editGraph[0][i-1] + gapPenalty
    #
    # for j in range (1, len(sequences[1]) - 3):
    #     editGraph[0][j] = editGraph[0][j-1] + gapPenalty

    traceback = []

    for i in range(len(sequences[0]) + 1):
        sub_matrix = [0]*(len(sequences[1]) + 1)
        traceback.append(sub_matrix) # this will help us create a 2D array for the matrix to hold information from both sequences

    for j in range(1, len(sequences[1]) + 1):
        traceback[0][j] = 'LEFT'

    for i in range(1, len(sequences[0]) + 1):
        traceback[i][0] = 'UP'

    for j in range(1, len(sequences[0]) + 1):
        for i in range(1, len(sequences[1]) + 1):
            editGraph[j][i] = max(editGraph[j-1][i-1] + int(scoreTheMatch(sequences[0][j-1], sequences[1][i-1])),
                                  editGraph[j][i-1] + gapPenalty,
                                  editGraph[j-1][i] + gapPenalty)

            if (max(editGraph[j - 1][i - 1] + int(scoreTheMatch(sequences[0][j-1], sequences[1][i-1])), editGraph[j][i - 1] + gapPenalty, editGraph[j - 1][i] + gapPenalty)
                == editGraph[j][i - 1] + gapPenalty):
                traceback[j][i] = 'LEFT'

            elif max(editGraph[j-1][i-1] + int(scoreTheMatch(sequences[0][j-1], sequences[1][i-1])),
                                  editGraph[j][i-1] + gapPenalty,
                                  editGraph[j-1][i] + gapPenalty) == editGraph[j-1][i] + gapPenalty:
                traceback[j][i] = 'UP'

            else:
                traceback[j][i] = 'DIAG'

            #FAULTY
            # if (max(editGraph[j - 1][i - 1] + int(matrix[matrixDictionary.get(sequences[0][j-1])][matrixDictionary.get(sequences[1][i-1])]), editGraph[j][i - 1] + gapPenalty, editGraph[j - 1][i] + gapPenalty)
            #     == editGraph[j - 1][i - 1] + int(matrix[matrixDictionary.get(sequences[0][j-1])][matrixDictionary.get(sequences[1][i-1])])):
            #     traceback[j][i] = 'DIAG'
            #
            # elif (max(editGraph[j - 1][i - 1] + int(matrix[matrixDictionary.get(sequences[0][j-1])][matrixDictionary.get(sequences[1][i-1])]), editGraph[j][i - 1] + gapPenalty, editGraph[j - 1][i] + gapPenalty)
            #     == editGraph[j][i - 1] + gapPenalty):
            #     traceback[j][i] = 'LEFT'
            #
            # else:
            #     traceback[j][i] = 'UP'


    traceback[0][0] = 'ORIGIN'
    return traceback, editGraph

#execution

sequenceFile = sys.argv[1]
matrixFile = sys.argv[2]
gapPenalty = int(sys.argv[3])

sequences = []
matrix = []

file_object = open(sequenceFile, "r")
for line in file_object:
    for word in line.split():
        sequences.append(word.upper())

file_object = open(matrixFile, "r")

matrix = np.genfromtxt(file_object, dtype='U25')

for line in file_object:
    row = []
    for number in line.split():
        row.append(number)
    matrix.append(row)

traceback, editGraph = getEditGraph(sequences, matrix, gapPenalty)

getAlignment(traceback, sequences, matrix, editGraph)


#while xLength > 0 or yLength > 0: