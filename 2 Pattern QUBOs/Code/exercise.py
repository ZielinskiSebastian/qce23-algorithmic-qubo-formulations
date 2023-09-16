from utils import calculateEnergy

"""
In this exercise you should complete the code of a function that checks whether a given 4x4 qubo is a clause qubo for a
given 3SAT clause.

This function is in the core of finding 3SAT qubos automatically. The algorithm for finding qubos for the 3SAT problem
automatically creates a huge amount of qubos (exhaustively) and the function you are completing below checks,
whether a given candidate qubo is indeed a correct clause qubo for a clause (which we are looking for).

As helping methods you can use:

calculateEnergy(sat_clause, sat_assignment, qubo) - which can be found in the utils.py if you want to take a look at the code
The argument sat_clause is a list, representing the given sat clause. i.e. [1,2,-3] represents the clause (x1 v x2 v -x3)

The argument sat_assignment is a list like [1, 0, 1] meaning the first variable of the sat clause got value 1, 
the second variable of the sat clause got value 0 and the last variable of the clause got value 1. I.e. if the
sat_clause = [1,2,-3] the assignment [1,0,1] would mean: x1 = 1 (true), x2 = 0 (false), -x3 = 1 (true) => x3 = 0 (false)

The argument qubo is a dictionary representing a qubo-matrix, like { (0,0) = 5, (0, 1) = 7, ... }
"""


def isClauseQUBO(sat_clause :list, qubo :dict):
    # A clause is a list of length 3, consisting of integer numbers.
    # examples: [-1, 5, 7] would be a clause meaning: (-x1 v x5 v x7)
    #           [2, -4, -16] would be a clause meaning: (x2 v -x4 v -16)

    # To begin, you need to find all satisfying and non-satisfying assignments of values to the variables  of a clause:
    # An assignment for a clause is a list of length 3 (as there are 3 variables in a sat clause), consisting of only
    # 0 and 1: example:
    #
    # if the clause is [1,2,-3] meaning the clause is (x1 v x2 v -x3) then
    # [1, 0, 0] would be a valid assignment meaning x1 = 1 (true), x2 = 0 (false), -x3 = 0 (false) => x3 = 1 (true)

    sat_assignments = []
    unsat_assignments = []

    # Complete the code below, such that sat_assignments is a list, containing all satisfying assignments
    # of a given clause and such tha unsat_assignments contains all non-satisfying assignments of a clause.
    # An assignment is also a list of length 3, containing only 0 and 1. Thus an examples for an assignment would be
    # [0, 0, 0] or [1, 0, 0] or [0, 1, 1] etc.
    #
    # sat_assignments is thus a list of lists like: [ [0, 0, 0], [1, 0, 0], ....] containing exactly 7 elements!
    # unsat_assignments is thus a list of lists like: [ [0, 1, 1] ] containing exactly 1 element!
    #
    # Which elements sat_assginments / unsat_assignments contain, depends on the sat_clause that is given as input

    # --------- start completing ---------



    # --------- end completing ---------

    # Now you need to find a condition that checks, whether the given QUBO is correctly representing the energy
    # spectrum of a 3SAT clause (hint: you need to use the sat_assignments /unsat_assignments list as well as the
    # calculateEnergy(sat_assignment :list, qubo :dict) function. If the qubo is indeed a clause qubo (your condition holds)
    # you should return true. If the qubo is not a clause qubo (your condition is false) you should return false
    # Hint 2: you are checking whether condition1 and condition2 in the slides hold

    # --------- start completing ---------


    # --------- end completing ---------



# -------------------- Run the exercise ------------------ #

clause = [1, 2, 3] # this represents the clause (x1 v x2 v x3)
# If you use "qubo_correct" with a clause, without negations the function "isClauseQUBO" should return true
# Careful: This qubo is only correct, if the clause has no negations!
qubo_correct = {(0,0): -2, (1,1): -2, (2,2): -2, (3,3): -2, (0, 1):1, (0,2): 1, (0, 3): 1, (1,2): 1, (1,3): 1, (2,3): 1}

# If you use "qubo_false" with a clause, without negations the function "isClauseQUBO" should return false
# qubo_false = {(0,0): -2, (1,1): -2, (2,2): -2, (3,3): -2, (0,1):1, (0,2): 1, (0, 3): 1, (1,2): 1, (1,3): 1, (2,3): 2}
print(isClauseQUBO(clause, qubo_correct))