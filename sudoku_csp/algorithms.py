# -*- coding: utf-8 -*-
"""Solver algorithms.

"""

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