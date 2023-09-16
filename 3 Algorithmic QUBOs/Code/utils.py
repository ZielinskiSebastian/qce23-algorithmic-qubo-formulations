from dwave_qbsolv import QBSolv
import random



# this function solves a given QUBO-Matrix Q with Qbsolv
def solve_with_qbsolv(Q):
    response = QBSolv().sample_qubo(Q, num_repeats=100)
    return response.samples()



# this function calculates the value of a solution for a given QUBO-Matrix Q
def getValue(Q, solution):
    ones = [x for x in solution.keys() if solution[x] == 1]
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
                print("      ", end = '')
                continue
            printing = ""
            if (row,column) in Q.keys() and Q[(row,column)] != 0:
                printing = str(Q[(row,column)])
            printing += "_____"
            printing = printing[:5]
            printing += " "
            print(printing, end = '')
        print("")



# this function checks, whether a given assignment satisfies a given SAT-formula
def check_solution(formula, assignment):
    for c in formula:
        sat = False
        for l in c:
            if l < 0 and assignment[abs(l)-1] == 0:
                sat = True
            elif l > 0 and assignment[abs(l)-1] == 1:
                sat = True
        if not sat:
            print(c) # print the clause which is not satisfied under the assignment
            return False
    return True



def add(Q, x, y, value):
    x = abs(x) - 1
    y = abs(y) - 1
    if x > y:
        x,y = y,x
    if (x,y) in Q.keys():
        Q[(x,y)] += value
    else:
        Q[(x,y)] = value

