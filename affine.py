import math
import sys
import numpy as np

#receiving input from the shell script
sequenceFile = sys.argv[1]
matrixFile = sys.argv[2]
gapOpeningPenalty = int(sys.argv[3])
gapExtensionPenalty = int(sys.argv[4])

#initializing all of these as global variables
sequences = []
scoringmatrix = []
matrixEPointers = []
matrixF = []
matrixG = []
matrixFPointers = []
matrixV = []
matrixVScoreTracker = []

#reading in the sequences
file_object = open(sequenceFile, "r")
for line in file_object:
    for word in line.split():
        sequences.append(word.upper())

file_object = open(matrixFile, "r")

#numpy import of the matrix scoring
scoringmatrix = np.genfromtxt(file_object, dtype='U25')

matrixE = []

#not super efficient but it works
def match(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return (i, j)


def scoreTheMatch(char1, char2):
    row = match(char1, scoringmatrix)[1]
    column = match(char2, scoringmatrix)[1]
    return scoringmatrix[row][column]


#initializes all arrays and the arrays used for point back trace back
def initializeArrays():
    # initializing E with values given in slides

    for i in range(len(sequences[0]) + 1):
        sub = [0] * (len(sequences[1]) + 1)
        matrixEPointers.append(sub)

    for i in range(len(sequences[0]) + 1):
        sub = [0] * (len(sequences[1]) + 1)
        matrixE.append(sub)
    # first row of E should be negative infinity

    matrixE[0] = [-math.inf] * (len(sequences[1]) + 1)

    # **** MAKE POINTERS
    # matrixE[1][1] = -3
    for i in range(1, (len(sequences[0]) + 1)):
        matrixE[i][0] = gapOpeningPenalty + (i * gapExtensionPenalty)
        matrixEPointers[i][0] = 'E'
    #matrixEPointers[1][0] = 'V'

    # initializing F with the values given in slides

    # ***MAKE POINTERS

    for i in range(len(sequences[0]) + 1):
        sub = [0] * (len(sequences[1]) + 1)
        matrixF.append(sub)

    for i in range(len(sequences[0]) + 1):
        matrixF[i][0] = -math.inf

    for i in range(len(sequences[0]) + 1):
        sub = [0] * (len(sequences[1]) + 1)
        matrixFPointers.append(sub)

    for i in range(1, (len(sequences[1]) + 1)):
        matrixF[0][i] = gapOpeningPenalty + (i * gapExtensionPenalty)
        matrixFPointers[0][i] = 'F'
    #matrixFPointers[0][1] = 'V'


    for i in range(len(sequences[0]) + 1):
        sub = [0] * (len(sequences[1]) + 1)
        matrixG.append(sub)

    # 0th column and rows should be filled with error values
    for i in range(len(sequences[1]) + 1):
        matrixG[0][i] = -1000000  # can change to a large negative number

    for i in range(len(sequences[0]) + 1):
        matrixG[i][0] = -1000000  # can change to a large negative number

    for i in range(len(sequences[0]) + 1):
        sub = [0] * (len(sequences[1]) + 1)
        matrixVScoreTracker.append(sub)

    # initialize matrix v with all zeros
    for i in range(len(sequences[0]) + 1):
        sub_matrix = [0] * (len(sequences[1]) + 1)
        matrixV.append(
            sub_matrix)  # this will help us create a 2D array for the matrix to hold information from both sequences

    for i in range(1, len(sequences[0]) + 1):
        matrixV[i][0] = matrixE[i][0]
        matrixVScoreTracker[i][0] = "E"
    for i in range(1, len(sequences[1]) + 1):
        matrixV[0][i] = matrixF[0][i]
        matrixVScoreTracker[0][i] = "F"


def recurrenceRelation():
    # g i,j is equal to v in some cases

    # creating backpointing trackers for v and f

    # keeping track of which matrix gave V each score

    #reccurence relation begins here
    for y in range(1, len(sequences[0]) + 1):
        for x in range(1, len(sequences[1]) + 1):

            # G does not need back pointers
            if sequences[0][y - 1] == sequences[1][x - 1]:
                matrixG[y][x] = matrixV[y - 1][x - 1] + int(scoreTheMatch(sequences[0][y - 1], sequences[1][x - 1]))
            else:
                matrixG[y][x] = matrixV[y - 1][x - 1] + int(scoreTheMatch(sequences[0][y - 1], sequences[1][x - 1]))

            matrixE[y][x] = max((matrixE[y - 1][x] + gapExtensionPenalty),
                                (matrixV[y - 1][x] + gapOpeningPenalty + gapExtensionPenalty))

            # filling in the pointer array for matrixE
            if matrixE[y][x] == matrixE[y - 1][x] + gapExtensionPenalty:
                matrixEPointers[y][x] = 'E'
            else:
                matrixEPointers[y][x] = 'V'

            matrixF[y][x] = max((matrixF[y][x - 1] + gapExtensionPenalty),
                                (matrixV[y][x - 1] + gapOpeningPenalty + gapExtensionPenalty))

            #backpointers for f and v
            if matrixF[y][x] == (matrixF[y][x - 1] + gapExtensionPenalty):
                matrixFPointers[y][x] = 'F'
            else:
                matrixFPointers[y][x] = 'V'

            matrixV[y][x] = max(matrixG[y][x], matrixE[y][x], matrixF[y][x])

            if matrixV[y][x] == matrixG[y][x]:
                matrixVScoreTracker[y][x] = 'G'
            elif matrixV[y][x] == matrixE[y][x]:
                matrixVScoreTracker[y][x] = 'E'
            else:
                matrixVScoreTracker[y][x] = 'F'


def traceback():
    x = len(sequences[1])
    y = len(sequences[0])

    xAlignment = []
    yAlignment = []
    maxScore = matrixV[y][x]
    current = matrixVScoreTracker[y][x]
    while (x > 0 or y > 0):

        if current == 'G':
            xAlignment.append(sequences[1][x-1])
            yAlignment.append(sequences[0][y-1])
            x = x - 1
            y = y - 1
            current = matrixVScoreTracker[y][x]
        elif current == 'V':
            current = matrixVScoreTracker[y][x]
        elif current == 'E':
            xAlignment.append('-')
            yAlignment.append(sequences[0][y-1])
            y = y - 1
            current = matrixEPointers[y][x]
        elif current == 'F':
            yAlignment.append('-')
            xAlignment.append(sequences[1][x-1])
            x = x - 1
            current = matrixFPointers[y][x]
    print(''.join(yAlignment[::-1]))
    print(''.join(xAlignment[::-1]))
    print(maxScore)

initializeArrays()
recurrenceRelation()
traceback()

