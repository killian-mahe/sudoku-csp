# -*- coding: utf-8 -*-
"""Solver algorithms.

"""
from sudoku_csp.csp import CSP


def backtracking_search(csp: CSP):
    """
    Implementation of the backtracking search algorithm.

    Parameters
    ----------
    csp : CSP
        The constraint satisfaction problem.

    Returns
    -------
    dict
    """
    return recursive_backtracking({}, csp)


def recursive_backtracking(assignment: dict, csp: CSP):
    """
    Recursive backtracking function.

    Parameters
    ----------
    assignment : dict
        Assignments of variables.
    csp : CSP
        The constraint satisfaction problem.

    Returns
    -------
    dict
    """
    if len(assignment) == len(csp.variables):
        return assignment

    var = select_unassigned_variable(assignment, csp)

    for value in order_domain_values(var, assignment, csp):
        if csp.consistent_with(assignment, {var: value}):
            assignment[var] = value
            result = recursive_backtracking(assignment, csp)
            if result is not None:
                return result
            assignment.pop(var)
    return None


def order_domain_values(var: any, assignment: dict, csp: CSP):
    """
    Get the domain values of a variable.

    Parameters
    ----------
    var : any
    assignment : dict
    csp : CSP

    Returns
    -------
    list[any]
    """
    return csp.domains[var]


def select_unassigned_variable(assignment: dict, csp: CSP):
    """
    Get a unselected variable.

    Parameters
    ----------
    assignment : dict
    csp : CSP

    Returns
    -------
    any
    """
    for var in csp.variables:
        if var not in assignment:
            return var
