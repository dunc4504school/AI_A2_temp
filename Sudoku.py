from __future__ import annotations

from collections import deque
from itertools import combinations
from typing import List, Optional, Set

from Constraint import Constraint
from Node import Node


class Sudoku:

    def __init__(self, path: str) -> None:
        self.constraints = None
        self.stat1 = ...
        self.stat2 = ...
        self.stat3 = ...
        self.board = self.create(path)
        self.initial_completed = self.get_completed_count()

    def create(self, path: str) -> List[List[Node]]:
        with open(path, "r") as file:
            sudoku = []
            for y, line in enumerate(file):
                row = line.strip().split(",")
                sudoku_row = [Node(x, y, start) for x, start in enumerate(row)]
                sudoku.append(sudoku_row)
        return sudoku

    def print_board(self) -> None:
        print(
            f"Completed(Initial): {self.get_completed_count()}({self.initial_completed})"
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

    def AC_3(self) -> bool:
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
        return True

    def get_completed_count(self) -> int:
        return sum(1 for row in self.board for node in row if len(node.domain) == 1)

    def is_solved(self) -> bool:
        """Check if the puzzle is solved (all domains have a single value)."""
        return all(len(node.domain) == 1 for row in self.board for node in row)

    def is_consistent(self, node: Node, value: int) -> bool:
        """Check if assigning 'value' to 'node' is consistent with Sudoku rules."""
        x, y = node.x, node.y

        # Check row
        for other_node in self.board[y]:
            if (
                other_node != node
                and len(other_node.domain) == 1
                and other_node.domain[0] == value
            ):
                return False

        # Check column
        for row in self.board:
            other_node = row[x]
            if (
                other_node != node
                and len(other_node.domain) == 1
                and other_node.domain[0] == value
            ):
                return False

        # Check 3x3 box
        box_start_x, box_start_y = 3 * (x // 3), 3 * (y // 3)
        for i in range(3):
            for j in range(3):
                other_node = self.board[box_start_y + i][box_start_x + j]
                if (
                    other_node != node
                    and len(other_node.domain) == 1
                    and other_node.domain[0] == value
                ):
                    return False

        return True

    def solve_with_backtracking(self) -> bool:
        """Solve the puzzle using backtracking if AC-3 doesn’t solve it."""
        if self.is_solved():
            return True  # Already solved

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
            if self.is_consistent(node, value):
                node.set_value(value)  # Assign the value
                if self.solve_with_backtracking():
                    return True
                node.reset_value()  # Reset if backtracking occurs

        return False

    def solve(self) -> None:
        """Solve the puzzle using AC-3, and if needed, backtracking."""
        if not self.AC_3() or not self.is_solved():
            if not self.solve_with_backtracking():
                print("No solution exists.")
            else:
                print("Solution found with backtracking.")
        else:
            print("Solution found with AC-3 alone.")

        self.print_board()
