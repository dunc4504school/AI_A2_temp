from __future__ import annotations

from collections import deque
from itertools import combinations
from typing import List, Optional, Set

from Constraint import Constraint
from Node import Node


class Sudoku:

    def __init__(self, path: str) -> None:
        
        self.board = self.create(path)
        self.constraints = None
        self.create_binary_constraints()

        self.initial_completed = self.get_completed_count()



    def create(self, path: str) -> List[List[Node]]:
        with open(path, "r") as file:
            sudoku = []
            for y, line in enumerate(file):
                row = line.strip().split(",")
                sudoku_row = [Node(x, y, start,self) for x, start in enumerate(row)]
                sudoku.append(sudoku_row)
        return sudoku

    def confirm_valid_initial_state(self):
        for constraint in self.constraints:
            if len(constraint.node1.domain) == 1 \
            and len(constraint.node2.domain) == 1 \
            and constraint.node1.domain[0] == constraint.node2.domain[0]:

                 return False

        return True


                


        
        



    def print_board(self) -> None:
        print(
            f"Completed(Initial): {self.get_completed_count()}/81({self.initial_completed})"
        )
        
        for row in self.board:
            print(",".join([node.get_state() for node in row]))

    def create_binary_constraints(self) -> None:
        constraint_index = set()
        constraints = list()

        # Row / Col constraints
        for dim1 in range(9):
            for dim21, dim22 in combinations(range(9), 2):
                constraint_index.add(((dim1, dim21), (dim1, dim22)))
                constraint_index.add(((dim21, dim1), (dim22, dim1)))

        # Box constraints
        for box_row in range(3):
            for box_col in range(3):
                cells = [
                    (3 * box_row + r, 3 * box_col + d)
                    for r in range(3)
                    for d in range(3)
                ]
                for n1, n2 in combinations(cells, 2):
                    constraint_index.add((n1, n2))

        for (x1, y1), (x2, y2) in sorted(list(constraint_index)):
            N1 = self.board[y1][x1]
            N2 = self.board[y2][x2]
            constraints.append(Constraint(N1, N2))
            constraints.append(Constraint(N2, N1))

        self.constraints = constraints

        for row in self.board:
            for node in row:
                node.set_constraints(self.constraints)

    def is_solved(self) -> bool:
        return self.get_completed_count() == 81

    def get_completed_count(self) -> int:
        return sum(1 for row in self.board for node in row if len(node.domain) == 1)

    def AC_3(self) -> Optional[bool]:
        queue = deque(self.constraints)
        queue_set = set(self.constraints)

        while queue:
            constraint = queue.popleft()
            queue_set.remove(constraint)

            if constraint.revise():
                if len(constraint.node1.domain) == 0:
                    return None
                else:
                    for neighbour_constraint in constraint.node1.constraints:
                        if neighbour_constraint not in queue_set:
                            queue.append(neighbour_constraint)
                            queue_set.add(neighbour_constraint)
        return self.is_solved()

    def BTS(self) -> Optional[bool]:
        """Solve the puzzle using backtracking if AC-3 doesn’t solve it."""

        # Select a variable (node) with the smallest domain > 1 (MRV heuristic)
        node = min(
            (node for row in self.board for node in row if len(node.domain) > 1),
            key=lambda n: len(n.domain),
            default=None,
        )

        if node is None:
            return True  # All variables are assigned

        # Iterate over a copy of the domain to try each possible value
        original_domain = node.domain.copy()
        for value in original_domain:
            if node.is_consistent(value):
                node.set_value(value)  # Assign the value
                if self.BTS():
                    return True
                node.reset_value()  # Reset if backtracking occurs

        return None



    def solve(self) -> None:

        #Already Solved
        if self.is_solved(): 
            print("Already Solved:")
            print("...")
        #Not Solved
        else:
            
            #Invalid Start
            if not self.confirm_valid_initial_state():
                print("Valid Start: No")
                print("...")
            #Valid Start
            else:
                print("Valid Start: Yes")
                print(f"Starting:    {self.initial_completed}")

                AC_3_result = self.AC_3()

                #Invalid Later
                if AC_3_result == None:
                    print("After AC_3:  Invalid Puzzle Discovered")
                    print("...")
                #Solved
                elif AC_3_result == True:
                    print("After AC_3:  81 - Solved")

                #Not Fully Solved
                else:
                    print(f"After AC_3:  {self.get_completed_count()}")

                    BTS_result = self.BTS()

                    #Invalid Later
                    if BTS_result == None:
                        print("After AC_3:   Invalid Puzzle Discovered")
                        print("...")
                    #Cant Continue, but valid????
                    elif BTS_result == False:
                        print(f"After BTS:  {self.get_completed_count()}")
                        ...
                    #Successed
                    else:
                        print("After BTS:   81 - Solved")
        print()
        self.print_board()