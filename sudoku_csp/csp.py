# -*- coding: utf-8 -*-
"""CSP representation.

"""

from interfaces import Constraint


class CSP:
    """
    A basic implementation of a CSP.
    """

    def __init__(self, variables: list, domains: dict, constraints: list):
        """
        Create a CSP instance.

        Parameters
        ----------
        variables : list
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
