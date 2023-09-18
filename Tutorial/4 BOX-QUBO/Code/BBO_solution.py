import numpy as np
import neal
from dwave_qbsolv import QBSolv
import random
import tensorflow as tf
import autoQ



def oracle(formula, assignment):
    sat = 0
    for clause in formula:
        for l in clause:
            if (l < 0 and assignment[abs(l) - 1] == 0) or (l > 0 and assignment[abs(l) - 1] == 1):
                sat += 1
                break
    return -sat


def create_random_formula(V, C, k):
    formula = []
    while len(formula) < C:
        clause = np.random.choice(range(1, V + 1), size=k, replace=False)
        sign = np.random.choice([-1, +1], size=k)
        clause *= sign
        clause.sort()
        clause = tuple(clause)
        if clause not in formula:
            formula.append(clause)
    return formula


def sample(formula, Q_dict, x_dim, n=50):
    # sample n solution vectors and predict y value
    sa_sampler = neal.SimulatedAnnealingSampler()
    samples = sa_sampler.sample_qubo(Q_dict, num_reads=n)
    X_star = samples.record['sample'].tolist()

    response = QBSolv().sample_qubo(Q_dict, num_repeats=100)
    xqubo = [response.samples()[0][i] for i in range(x_dim)]
    X_star.append(xqubo)

    Y_star = [oracle(formula, x) for x in X_star]

    return X_star, Y_star


def optimize(formula, init_X, init_Y, ratio, training_length):
    Q = autoQ.autoQ(np.copy(init_X), np.copy(init_Y), ratio)

    Q.test(100)

    Q.train(20, 400)
    chart = [np.min(Q.Y)]

    for e in range(training_length):

        print("#### Iteration", e, "####")
        #Q.test(100)
        print("BOX-QUBO chart: ", chart)

        Q_dict, _ = Q.get_Q()
        X_star, Y_star = sample(formula, Q_dict, x_dim=len(init_X[0]))
        Q.add(X_star, Y_star)
        Q.train(10, 200)
        chart.append(np.min(Q.Y))


seed = 99
np.random.seed(seed)
random.seed(seed)
tf.random.set_seed(seed)


init_trainings_size = 100
V, C, k = 15, 100, 3

formula = create_random_formula(V, C, k)

init_X = np.random.choice(2, size=(init_trainings_size, V), p=[0.5, 0.5]).tolist()
init_Y = np.array([oracle(formula, x) for x in init_X])

optimize(formula, init_X, init_Y, 0.3, 15)


