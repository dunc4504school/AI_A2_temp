from __future__ import annotations
from typing import Callable, List, Optional, Tuple, Set

class Node:
    #Creates a Node Object To Store A Single Square
    def __init__(self, x: int, y: int, starting: str, sudoku: Sudoku) -> None:
        self.x, self.y = x, y
        self.sudoku = sudoku
        self.constraints = None
        self.domain = self.get_initial_domain(starting)
        self.initial = len(self.domain) == 1

    #Returns the nodes initial domain (known value, or all possibilitys)
    def get_initial_domain(self, starting: str) -> List[int]:
        return [int(starting)] if starting != '_' else list(range(1, 10))

    #Creates The List Of All Constaints, Associated With This Node
    def set_constraints(self, constraints: List[Constraint]) -> None:
        self.constraints = [constraint for constraint in constraints if constraint.node2 == self]

    #Sets The Confirmed Value Of A Node (by reducing its domain accordingly)
    def set_value(self, value: int) -> None:
        self.domain = [value]

    #Resets domain to all possibilities (except when initially known)
    def reset_value(self) -> None:
        if not self.initial: self.domain = list(range(1, 10))

    #Returns whether a value, keeps its associated constraints consistent
    def is_consistent(self, value) -> bool:
        for c in self.constraints:
            if len(c.node1.domain) == 1 and c.node1.domain[0] == value: return False
        return True






    #Returns The Domain (unknown, or known value) for string output
    def get_state(self, distinguish_initial) -> str:
        if len(self.domain) != 1 :
            return '_'
        
        else:
            if not distinguish_initial:
                return str(self.domain[0])
            else:

                if self.initial:
                    return f"[{str(self.domain[0])}]"
                else:
                    return f'_{str(self.domain[0])}_'
        

    #Creates A String Output For Node
    def __str__(self) -> str:
        return f"y:{self.y} x:{self.x} " + f"d:[{','.join(map(str, self.domain))}]"

    #Prints The Constraints Associated With This Node
    def print_constraints(self) -> None:
        for con in self.constraints:
            print(f"  {str(con)}")
