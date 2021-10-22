"""
Main app interfaces.
"""

from enum import Enum


class AlgorithmType(Enum):
    BACKTRACKING = "Backtracking"
    MRV = "MRV"
    AC3 = "AC-3"
    DEGREE_H = "Degree heuristic"
    LEAST_CONSTRAINING_H = "Least constraining value"
