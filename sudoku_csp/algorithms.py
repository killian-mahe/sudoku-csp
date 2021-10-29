# -*- coding: utf-8 -*-
"""Solver algorithms.

"""
from sudoku_csp.csp import CSP
from sudoku_csp.interfaces import Constraint


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


def minimum_remaining_value(assignment, csp: CSP):
    min_value_count = 0
    selected_var = None
    for var in csp.variables:
        if var not in assignment:
            if not min_value_count or len(csp.domains[var]) < min_value_count:
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


def most_constrained_variable(assignment: dict, csp: CSP):
    unassigned_variables = csp.variables.symmetric_difference(set(assignment.keys()))

    unassigned_var_to_const = {
        k: csp.var_to_const[k] for k in unassigned_variables if k in csp.var_to_const
    }

    return sorted(unassigned_var_to_const, key=len)[0]


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
