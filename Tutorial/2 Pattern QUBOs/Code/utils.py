from dimod.utilities import qubo_energy

def calculateEnergy(sat_clause: list, sat_assignment : list, qubo :dict):

    # we assume that the negation is always at the end -> sort clause (and assignment) list
    clause_assignment_tuple_list = list(zip(sat_clause, sat_assignment))
    clause_assignment_tuple_list.sort(key=lambda values: values[0], reverse=True)
    sat_clause, sat_assignment = zip(*clause_assignment_tuple_list)

    # there is an aniclla in a 4x4 qubo -> each sat assignment corresponds to 2 bitstrings
    assignment_dict1 = {index: value for index, value in enumerate(sat_assignment)}
    assignment_dict1[3] = 0

    assignment_dict2 = {index: value for index, value in enumerate(sat_assignment)}
    assignment_dict2[3] = 1

    return min(qubo_energy(assignment_dict1, qubo), qubo_energy(assignment_dict2, qubo))
