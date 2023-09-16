import utils
import math
import numpy as np
import copy
import matplotlib.pyplot as plt
import itertools



def OR(Q, c):
    if list(np.sign(c)) == [1, 1]:
        utils.add(Q, abs(c[0]), abs(c[0]), -1)
        utils.add(Q, abs(c[1]), abs(c[1]), -1)
        utils.add(Q, abs(c[0]), abs(c[1]), 1)
    elif list(np.sign(c)) == [1, -1]:
        utils.add(Q, c[0], c[1], -1)
        utils.add(Q, c[1], c[1], 1)
    else:
        utils.add(Q, c[0], c[1], 1)
        
        
def SAT3(Q, c, a):
    if list(np.sign(c)) == [1, 1, 1]:
        utils.add(Q, c[0], c[1], 2)
        utils.add(Q, c[0], a, -2)
        utils.add(Q, c[1], a, -2)
        utils.add(Q, c[2], c[2], -1)
        utils.add(Q, c[2], a, 1)
        utils.add(Q, a, a, 1)
    elif list(np.sign(c)) == [1, 1, -1]:
        utils.add(Q, c[0], c[1], 2)
        utils.add(Q, c[0], a, -2)
        utils.add(Q, c[1], a, -2)
        utils.add(Q, c[2], c[2], 1)
        utils.add(Q, c[2], a, -1)
        utils.add(Q, a, a, 2)
    elif list(np.sign(c)) == [1, -1, -1]:
        utils.add(Q, c[0], c[0], 2)
        utils.add(Q, c[0], c[1], -2)
        utils.add(Q, c[0], a, -2)
        utils.add(Q, c[1], a, 2)
        utils.add(Q, c[2], c[2], 1)
        utils.add(Q, c[2], a, -1)
    else:
        utils.add(Q, c[0], c[0], -1)
        utils.add(Q, c[0], c[1], 1)
        utils.add(Q, c[0], c[2], 1)
        utils.add(Q, c[0], a, 1)
        utils.add(Q, c[1], c[1], -1)
        utils.add(Q, c[1], c[2], 1)
        utils.add(Q, c[1], a, 1)
        utils.add(Q, c[2], c[2], -1)
        utils.add(Q, c[2], a, 1)
        utils.add(Q, a, a, -1)


class kSAT:

    def __init__(self, formula, V):
        # sort the formula (i.e. all negative literals are at the back of the clause)
        self.formula = [sorted(c, reverse=True) for c in formula]
        self.V = V
        self.Q = {}

    # this function creates the QUBO-Matrix Q
    def fillQ(self):
        a = self.V + 1 # a points to the next ancilla
        formula = copy.deepcopy(self.formula) # copy in order to keep self.formula unchanged
        for c in formula:
            if len(c) == 2:
                OR(self.Q, c)
            elif len(c) == 3:
                SAT3(self.Q, c, a)
                a += 1
            else:
                h = math.ceil(math.log2(len(c) + 1))
                var = [abs(l) for l in c]
                var.extend([a+i for i in range(h)])
                val = [np.sign(l) for l in c]
                val.extend([-(2**i) for i in range(h)])
                n =  len([1 for l in c if l < 0]) # number of negated literals
                for l1 in range(len(var)):
                    utils.add(self.Q, var[l1], var[l1], 2*n*val[l1])
                    for l2 in range(len(var)):
                        utils.add(self.Q, var[l1], var[l2], val[l1]*val[l2])
                formula.append([a+i for i in range(h)])
                a += h

        print("Size of QUBO Matrix: ", a-1)
        utils.printQUBO(self.Q, a-1)

    # this function starts creating Q, solving it and interpreting the solution
    # (e.g. deciding whether the formula is satisfiable or not)
    def solve(self):
        self.fillQ()

        buckets = [0] * 64
        labels = [str(z) for z in list(itertools.product([0, 1], repeat=self.V))]

        for r in range(200):
            answer = utils.solve_with_qbsolv(self.Q)
            for z in answer:
                assignment = [z[i] for i in range(self.V)]
                i = np.dot([2**k for k in range(6)], assignment)
                buckets[i] += 1
            if r%10 == 0:
                print(r)

        plt.bar(labels, buckets)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(left=0.068, bottom=0.2, right=0.986, top=0.9, wspace=0.166, hspace=0.17)
        plt.show()



V = 6
formula = [[1,-2,3,4,-5,6]]
print(formula)
kSAT(formula, V).solve()


V = 30
formula = [[i+1 for i in range(30)]]
print(formula)
kSAT(formula, V).fillQ()
