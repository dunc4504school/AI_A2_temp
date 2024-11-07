from __future__ import annotations
from typing import Callable, List, Optional, Tuple, Set




class Node:
    def __init__(self, x: int, y: int, starting: str) -> None:
        self.x = x
        self.y = y
        self.constraints = None
        self.domain = self.get_initial_domain(starting)
        self.initial = len(self.domain) == 1

    def __str__(self) -> str:
        return f"y:{self.y} x:{self.x} " + f"[{','.join(map(str, self.domain))}]"

    def get_state(self) -> str:
        return '_' if len(self.domain) > 1 else str(self.domain[0])

    def print_constraints(self) -> None:
        for con in self.constraints:
            print(f"  {str(con)}")

    def get_initial_domain(self, starting: str) -> List[int]:
        return [int(starting)] if starting != '_' else list(range(1, 10))

    def set_constraints(self, constraints: List[Constraint]) -> None:
        self.constraints = [constraint for constraint in constraints if constraint.node2 == self]

    def set_value(self, value: int) -> None:
        """Sets the node's domain to a single value."""
        self.domain = [value]

    def reset_value(self) -> None:
        """Resets the node's domain to its full range (1-9) if it was initially empty."""
        if not self.initial:
            self.domain = list(range(1, 10))
