# -*- coding: utf-8 -*-
"""Solver algorithms.

"""
from sudoku_csp.csp import CSP
from sudoku_csp.interfaces import Constraint


def recursive_backtracking(csp: CSP, assignment: dict, var_selector):
    if len(assignment) == len(csp.variables):
        return assignment
    unassigned_var = var_selector(assignment, csp)
    for value in csp.domains:
        assignment[unassigned_var] = value
        if csp.consistent(assignment):
            result = recursive_backtracking(csp, assignment, var_selector)
            if result is not None: return result
            assignment.pop(unassigned_var)
    return None


def naive_selector(assignment, csp: CSP):
    for var in csp.variables:
        if var not in assignment:
            return var


def minimum_remaining_value(assignment, csp: CSP):
    min_value_count = 0
    selected_var = None
    for var in csp.variables:
        if var not in assignment:
            if min_value_count == 0 or len(csp.domains[var]) < min_value_count:
                selected_var = var
                min_value_count = len(csp.domains[var])
    return selected_var


def AC3(csp: CSP) -> CSP:
    def remove_inconsistent_values(v, associated_constraint: Constraint) -> bool:
        removed = False
        for value in csp.domains[v]:
            for other_var in associated_constraint.scope:
                if other_var != v:
                    violated = True
                    for other_value in csp.domains[other_var]:
                        if associated_constraint.satisfied({v: value, other_var: other_value}):
                            violated = False
                            break
                    if violated:
                        csp.domains[v].remove(value)
                        removed = True
        return removed

    arcs = csp.var_to_const.copy()
    while len(arcs) > 0:
        (var, associated_constraints) = arcs.popitem()
        for constraint in associated_constraints:
            if remove_inconsistent_values(var, constraint):
                for affected in csp.neighbour(var):
                    arcs[affected] = csp.var_to_const[affected]

    return csp
