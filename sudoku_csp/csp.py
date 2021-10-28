# -*- coding: utf-8 -*-
"""CSP representation.

"""
import math

import numpy as np

from interfaces import Constraint


class CSP:
    """
    A basic implementation of a CSP.
    """

    def __init__(self, variables: set, domains: dict, constraints: list):
        """
        Create a CSP instance.

        Parameters
        ----------
        variables : set
            The list of variables.
        domains : dict
            A dictionary containing the domain of each variable.
        constraints : list
            A list of constraint.
        """
        self.domains = domains
        self.variables = variables
        self.constraints = constraints

        self.var_to_const = {var: set() for var in self.variables}

        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def add_constraints(self, constraint: Constraint):
        """
        Add a new constraint.

        Parameters
        ----------
        constraint : Constraint
            The list of constraints to add.

        Returns
        -------
        None
        """
        for var in constraint.scope:
            if var in self.variables:
                self.var_to_const[var].add(constraint)

    def consistent(self, assignment: dict):
        """
        Check if the passed assignment is consistent regarding the CSP.

        Parameters
        ----------
        assignment : dict
            A dictionary {var: domain} representing the assignments of a CSP.

        Returns
        -------
        bool
        """
        return all(
            con.satisfied(assignment)
            for con in self.constraints
            if all(v in assignment for v in con.scope)
        )


class SudokuCSP(CSP):
    def __init__(self, sudoku_map: np.ndarray):

        def constraint_evalution(a: int, b: int):
            return a != b

        variables = set()
        domains = dict()
        constraints = list()

        size = round(math.sqrt(len(sudoku_map)))

        for x in range(len(sudoku_map)):
            for y in range(len(sudoku_map)):
                variables.add(f"{x}, {y}")
                domain = set(range(1, 10)) if not sudoku_map[x, y] else {sudoku_map[x, y]}
                domains[f"{x}, {y}"] = domain

                for x_row in range(len(sudoku_map)):
                    constraint = Constraint(frozenset({f"{x}, {y}", f"{x_row}, {y}"}), constraint_evalution)
                    if constraint not in constraints:
                        constraints.append(constraint)

                for y_col in range(len(sudoku_map)):
                    constraint = Constraint(frozenset({f"{x}, {y}", f"{x}, {y_col}"}), constraint_evalution)
                    if constraint not in constraints:
                        constraints.append(constraint)

                for i in range(size):
                    constraint = Constraint(frozenset({f"{x}, {y}", f"{x % size + i}, {y % size + i}"}), constraint_evalution)
                    if constraint not in constraints:
                        constraints.append(constraint)

        super().__init__(variables, domains, constraints)

    # def recursive_backtracking(self, assignment):
    #     if len(assignment) == len(self.variables):
    #         return assignment
    #     unassigned_var = 0
    #     for var in self.variables:
    #         if var not in assignment:
    #             unassigned_var = var
    #     for value in self.domains:
    #         test_assignment = assignment.copy()
    #         test_assignment[unassigned_var] = value
    #         if self.consistent(test_assignment, unassigned_var):
    #             assignment[unassigned_var] = value
    #         result = self.recursive_backtracking(assignment)
    #         if result is not None:
    #             return result
    #     return None
