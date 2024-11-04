from __future__ import annotations
from typing import Callable, List, Optional, Tuple, Set
from itertools import combinations
from collections import deque

from Node import Node
from Constraint import Constraint

class Sudoku:

    def __init__(self,path: str) -> None:
        self.constraints = None
        self.stat1 = ...
        self.stat2 = ...
        self.stat3 = ...
        self.board = self.create(path)

        self.initial_completed = self.get_completed_count()

    def create(self,path: str) -> List[List[Node]]:
        with open(path, 'r') as file:
            sudoku = []
            for y, line in enumerate(file):
                row = line.strip().split(',')
                sudoku_row = [Node(x,y, start) for x, start in enumerate(row)]
                sudoku.append(sudoku_row)  
        return sudoku

    def print_board(self) -> None:
        print(f"Completed(Initial): {self.get_completed_count()}({self.initial_completed})")
        for row in self.board:
            print(','.join([node.get_state() for node in row]))

    def create_binary_constraints(self) -> None:

        constraint_index = set()
        constraints = list()
        
        #Row / Col
        for dim1 in range(9):
            for dim21,dim22 in combinations(range(9),2):
                constraint_index.add(((dim1,dim21), (dim1,dim22)))
                constraint_index.add(((dim21,dim1), (dim22,dim1)))
                
        #Boxs
        for box_row in range(3):
            for box_col in range(3):
                cells = [(3 * box_row + r, 3 * box_col + d) for r in range(3) for d in range(3)]
                for n1, n2 in combinations(cells,2):
                    constraint_index.add((n1, n2))
                    

        for (x1,y1), (x2,y2) in sorted(list(constraint_index)):
            N1 = self.board[y1][x1]
            N2 = self.board[y2][x2]
            constraints.append(Constraint(N1,N2))
            constraints.append(Constraint(N2,N1))

        self.constraints = constraints

        for row in self.board:
            for node in row:
                node.set_constraints(self.constraints)        

    def AC_3(self) -> None:

        queue = deque(self.constraints)
        queue_set = set(self.constraints)

        while queue:

            constraint = queue.popleft()
            queue_set.remove(constraint)

            if constraint.revise():

                if len(constraint.node1.domain) == 0:
                    return False
                else:
                    for neighbour_constraint in constraint.node1.constraints:

                        if neighbour_constraint not in queue_set:
                            queue.append(neighbour_constraint)
                            queue_set.add(neighbour_constraint)

    def get_completed_count(self) -> int:
        return sum(1 for row in self.board for node in row if len(node.domain) == 1)

        