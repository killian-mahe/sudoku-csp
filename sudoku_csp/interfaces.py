# -*- coding: utf-8 -*-
"""Application interfaces.

This module regroup all the differents enumeration, interfaces and abstract
class of the application.

"""

from enum import Enum

from PySide6.QtCore import Signal, QObject


class AlgorithmType(Enum):
    BACKTRACKING = "Backtracking"
    MRV = "MRV"
    AC3 = "AC-3"
    DEGREE_H = "Degree heuristic"
    LEAST_CONSTRAINING_H = "Least constraining value"


class Resolver(QObject):
    """
    A worker who manage the resolving of a problem.
    """

    result_ready = Signal()

    def do_work(self):
        self.result_ready.emit()


class Constraint:
    """
    A constraint is composed of a set of variable where the constraint applied
    and a evaluation function.
    """

    def __init__(self, scope: list, val_func: callable):
        """
        Create a Constraint instance.

        Parameters
        ----------
        scope : list
            The list of variables where the constraint is applied.
        val_func : callable
            The evaluation function.
        """
        self.scope = scope
        self.val_func = val_func

    def satisfied(self, assignment: dict):
        """
        Check if the constraint is satisfied in the given assignment.

        Parameters
        ----------
        assignment : dict
            The assignment to check.

        Returns
        -------
        bool
        """
        return self.val_func(*tuple(assignment[v] for v in self.scope))
