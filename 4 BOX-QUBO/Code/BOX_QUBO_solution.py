import numpy as np
import itertools
import utils
import autoQ




init_X = np.array(list(itertools.product([0, 1], repeat=10)))

init_Y = []
for i in range(len(init_X)):
    z1 = np.dot([2**(4-k) for k in range(5)], init_X[i][0:5])
    z2 = np.dot([2**(4-k) for k in range(5)], init_X[i][5:10])
    if 0 <= z1 - z2 <= 2:
        init_Y.append(0)
    else:
        init_Y.append(1)
init_Y = np.array(init_Y)



Q = autoQ.autoQ(init_X, init_Y, 1)
Q.train(n_cycles=500, n_epochs=50)
Q.test(1000)

utils.printQUBO(Q.get_Q()[0], 10)

