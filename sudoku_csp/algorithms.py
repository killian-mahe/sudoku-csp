# -*- coding: utf-8 -*-
"""Solver algorithms.

"""
from sudoku_csp.csp import CSP


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

