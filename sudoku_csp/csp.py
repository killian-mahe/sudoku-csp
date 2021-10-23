# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 14:17:08 2021

@author: Nomanina
variables : each case of the sudoku grid
domain : [1,9]
domain
"""



class Constraint:
    def __init__(self, variables):
        self.variables = variables
    def satisfied(self, assignement):
        pass
    
        
class CSP:
    def __init__(self, variables, domains):
        self.domains = domains
        self.variables = variables
        self.constraints = {}
        for var in variables:
            if(var in self.domains):
                self.constraints[var] = []
        
        
    def add_constraints(self,constraint):
        for var in constraint.variables:
            if var in self.variables:
                self.constraints[var].append(constraint)
    
    def consistent(self, assignement,variable):
        for constraint in assignement[variable]:
            if(not constraint.satisfied(assignement)):
                return False
        return True           
        
    def recursive_backtracking(self,assignement):
        if len(assignement) == len(self.variables):
            return assignement     
        unassigned_var = 0
        for var in self.variables:
            if var not in assignement:
                unassigned_var = var     
        for value in self.domains:
            test_assignement = assignement.copy()
            test_assignement[unassigned_var] = value          
            if(self.consistent(test_assignement,unassigned_var)):
                assignement[unassigned_var] = value
            result = self.recursive_backtracking(assignement)
            if(result != None):
                return result
        return None
    
    
    
                
            
            
    
    
        