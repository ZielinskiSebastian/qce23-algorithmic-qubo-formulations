from dwave_qbsolv import QBSolv
import random



# this function solves a given QUBO-Matrix Q with Qbsolv
def solve_with_qbsolv(Q):
    response = QBSolv().sample_qubo(Q, num_repeats=100)
    return response.samples()



# this function calculates the value of a solution for a given QUBO-Matrix Q
def getValue(Q, solution):
    ones = [i for i in range(len(solution)) if solution[i] == 1]
    value = 0
    for x in ones:
        for y in ones:
            if (x,y) in Q.keys():
                value += Q[(x,y)]
    return value



# this function prints the first n row/columns of a QUBO-Matrix Q
def printQUBO(Q, n):
    for row in range(n):
        for column in range(n):
            if row > column:
                print("        ", end = '')
                continue
            printing = ""
            if (row,column) in Q.keys() and Q[(row,column)] != 0:
                printing = str(float(Q[(row,column)]))
            printing += "_______"
            printing = printing[:7]
            printing += " "
            print(printing, end = '')
        print("")


