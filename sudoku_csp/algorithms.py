# -*- coding: utf-8 -*-
"""Solver algorithms.

"""
from sudoku_csp.csp import CSP


def unorder_domain_values(var: any, assignment: dict, csp: CSP):
    """
    Get the domain values of a variable in a random order.

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


def first_unassigned_variable(assignment: dict, csp: CSP):
    """
    Get the first unselected variable.

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


def backtracking_search(
    csp: CSP,
    select_unassigned_variable=first_unassigned_variable,
    order_domain_values=unorder_domain_values,
):
    """
    Implementation of the backtracking search algorithm.

    Parameters
    ----------
    csp : CSP
        The constraint satisfaction problem.
    select_unassigned_variable : callable
        How the variables are sorted.
    order_domain_values : callable
        How the domain ise sorted.

    Returns
    -------
    dict
    """
    return recursive_backtracking(
        {}, csp, select_unassigned_variable, order_domain_values
    )


def recursive_backtracking(
    assignment: dict,
    csp: CSP,
    select_unassigned_variable=first_unassigned_variable,
    order_domain_values=unorder_domain_values,
):
    """
    Recursive backtracking function.

    Parameters
    ----------
    assignment : dict
        Assignments of variables.
    csp : CSP
        The constraint satisfaction problem.
    select_unassigned_variable : callable
        How the variables are sorted.
    order_domain_values : callable
        How the domain ise sorted.

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
