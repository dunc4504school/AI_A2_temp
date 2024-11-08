from __future__ import annotations

from typing import Callable, List, Optional, Set, Tuple

from Node import Node


class Constraint:
    def __init__(self, node1: Node, node2: Node) -> None:
        self.node1 = node1
        self.node2 = node2

    def __str__(self) -> str:
        return f"{str(self.node1):<29} != {str(self.node2)}"

    def revise(self) -> bool:
        change = False

        for possibility in self.node1.domain:
            # TODO: confirm this is best solution?????/
            if len(self.node2.domain) == 1 and self.node2.domain[0] == possibility:
                self.node1.domain.remove(possibility)
                change = True

        return change
