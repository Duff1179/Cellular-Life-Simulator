"""
=============================================================================
Title : final_project.py
Description : 100 iteration matrix calcualtor for a celluar life simulator
Author : Dylan Duffey (R11868447)
Date : 05/06/2025
Version : 2.0
Usage : Run using Python 3.13.2
Notes : No other dependencies, but takes -i as an input file -o as a output file and -p (optional) as a processor count
Python Version : 3.13.2
=============================================================================
"""
import argparse
from pathlib import Path
from copy import deepcopy
from math import sqrt
import multiprocessing as mp
import time #TEMPORARY

fib_pre = {0, 1, 2, 3, 5, 8, 13, 21}
pow2_pre = {1, 2, 4, 8, 16}
prime_pre = {2, 3, 5, 7, 11, 13, 17, 19, 23}

def main():
    start = time.time()#TEMP
    print("Project :: R11868447")

    #Taking in arguments and checking their validity
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file path")
    parser.add_argument("-o", help="Output file path")
    parser.add_argument("-p", help="Number of processes (optional)", type=int)
    args = parser.parse_args()

    if args.p: #if you give how many processes you want
        prcsCount = args.p
    else: #otherwise we assume 1
        prcsCount = 1

    if prcsCount < 1: #checking positive processor count
        print("Error, processor count must be a postive number\n")
        exit()
    if not args.i or not args.o: #checking if you give proper -i and -o
        print("Error, please provide -i (input file) and -o (output file)\n")
        exit()
    fin = Path(args.i)
    fout = Path(args.o)
    if not fin.is_file(): #checking for valid input file
        print("Error, input file does not exist\n")
        exit()

    #taking the file and reading it
    file = open(fin, "r")
    lines = len(file.readlines()) #matrix size
    file.seek(0) #rewind the file pointer to take it as input
    mtx = MtxIn(file, lines) #read file

    #Mulitprocessing and splitting up the matrix
    split = int(lines/prcsCount) #split the rows up
    processPool = mp.Pool(processes=prcsCount)

    #below is the iterable inputs to the starmap (mtx, boundLX, boundLY, boundUX, size)
    arguments = [(mtx, run, 0, run + split, lines) \
                    for run in range(0, lines, split)]
    
    for i in range(1,101):
        results = processPool.starmap(MtxIterate, arguments) #scatter gather process (for one iteration of the cycle)
        #recieve results
        #taking each result (each processes' return) and appending each row from it to the mtx
        mtx.clear() 
        for result in results:
            for row in result:
                mtx.append(row)
    processPool.close()

    #outputting the new file
    MtxOut(mtx, fout)
    file.close()
    print("Time: ", time.time()-start)#TEMP


#takes a "lines" size matrix and reads it line by line from a file
def MtxIn(file, lines):
    mtxt = []
    for i in range(lines): #create each row of the matrix
        row = []
        for j in range(lines+1): #adding one to lines for the new line characters
            char = file.read(1)
            if(char == "O"):
                row.append(3)
            elif(char == "o"):
                row.append(1)
            elif(char == "."):
                row.append(0)
            elif(char == "x"):
                row.append(-1)
            elif(char == "X"):
                row.append(-3)
        mtxt.append(row)
    return mtxt

#outputs a matrix to the output file
def MtxOut(matrix, path):
    output = open(path, "w")
    for row in matrix: #get each row of the matrix
        for col in row: #get each column of the singular row
            if col == 3:
                output.write("O")
            elif col == 1:
                output.write("o")
            elif col == 0:
                output.write(".")
            elif col == -1:
                output.write("x")
            elif col == -3:
                output.write("X")
        output.write("\n") #new line after each row
    output.close()

#runs one descirbed iteration of the celluar life simulator
def MtxIterate(mtx, boundLX, boundLY, boundUX, size):
    
    #input creation
    currX = boundLX
    currY = boundLY
    if boundUX > size: #ensure boundUX is not bigger than size (incase run + split returns over size)
        boundUX = size
    mtxCng = []

    #run though each column of the matrix until you hit the ending bound (boundUX)
    while currX < boundUX:
            row = []
            while currY < size:
                currCell = mtx[currX][currY] #get the current cell

                '''
                Summing all the neighbors around the current cell
                Checking possible out of bounds (if you go over the array size) and adjusting the neighbors accordingly
                Anything with currX+1/currY+1 can go above the size of the matrix, so they get overriden to zero if necessary
                '''

                nbrSum = 0
                #normal (neither are larger than matrix size)
                if currX + 1 < size and currY + 1 < size:
                    nbrSum += mtx[currX-1][currY+1]
                    nbrSum += mtx[currX][currY+1]
                    nbrSum += mtx[currX+1][currY-1] 
                    nbrSum += mtx[currX+1][currY]
                    nbrSum += mtx[currX+1][currY+1] 

                #currY + 1 goes larger than the matrix size
                elif currX + 1 < size:
                    nbrSum += mtx[currX+1][currY-1]
                    nbrSum += mtx[currX+1][currY]
                    nbrSum += mtx[currX-1][0]
                    nbrSum += mtx[currX][0]
                    nbrSum += mtx[currX+1][0]

                #currX + 1 goes larger than the matrix size
                elif currY + 1 < size: 
                    nbrSum += mtx[currX-1][currY+1]
                    nbrSum += mtx[currX][currY+1]
                    nbrSum += mtx[0][currY-1]
                    nbrSum += mtx[0][currY]
                    nbrSum += mtx[0][currY+1]

                #currX + 1 and currY + 1 go larger than the matrix size
                else:
                    nbrSum += mtx[currX-1][0]
                    nbrSum += mtx[currX][0]
                    nbrSum += mtx[0][currY-1]
                    nbrSum += mtx[0][currY]
                    nbrSum += mtx[0][0]

                #these wrap natively in python, so no changes for these below (negative indicies)
                nbrSum += mtx[currX-1][currY-1]
                nbrSum += mtx[currX-1][currY]
                nbrSum += mtx[currX][currY-1]

                '''
                Doing the celluar life simulation (dependent on each current state and the nbrSum)
                '''
                #if the current cell is a big O
                if currCell == 3:
                    #checking if the nbrSum is in the pre-calculated fib set             
                    if nbrSum in fib_pre:
                        currCell = 0 #O to dead
                    elif nbrSum < 12:
                        currCell = 1 #O to o

                #if the current cell is little O       
                elif currCell == 1:
                    if nbrSum < 0:
                        currCell = 0 #o to dead
                    elif nbrSum > 6:
                        currCell = 3 #o to O

                #if the current cell is dead
                elif currCell == 0:
                    #check if nbrSum or the abs value is in the pre-calculated powers of 2
                    if nbrSum in pow2_pre:
                        currCell = 1 #dead to o
                    elif abs(nbrSum) in pow2_pre:
                        currCell = -1 #dead to x

                #if the current cell is little x
                elif currCell == -1:
                    if nbrSum > 0:
                        currCell = 0 #x to dead
                    elif nbrSum < -6:
                        currCell = -3 #x to X
                
                #if the current cell is big X
                elif currCell == -3:
                    #check if the absolute value of nbrSum is in the pre-calculated primes
                    if abs(nbrSum) in prime_pre:
                        currCell = 0 #X to dead
                    elif nbrSum > -12:
                        currCell = -1 #X to x
                
                #updating the new mtx to it's new cell, we keep the input the same as we have to check each cell before ANY cells change
                #then we move on to the next cell until we've hit our bounds
                row.append(currCell)
                currY += 1
            currY = 0
            mtxCng.append(row)
            currX += 1
    #return the new matrix      
    return mtxCng

#ends function MtxIterate (or one iteration of the celluar life simulation)


if __name__ == "__main__":
    main()