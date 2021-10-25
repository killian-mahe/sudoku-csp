# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 21:09:23 2021

@author: Nomanina
"""

from csp import Constraint, CSP

class SudokuConstraint(Constraint):
    def __init__(self,variables):
        super().init(variables)
        
    def satisfied(self,assignement):
        values = []
        dict = {}
        for i in range (len(assignement)):
            values[i] = assignement[i]
        for value in values:
            if dict[value] == None:
                dict[value] = value
            else:
                return False
        return True
    

        
        
    