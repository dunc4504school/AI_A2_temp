from __future__ import annotations

from collections import deque
from itertools import combinations
from typing import List, Optional, Set

from Constraint import Constraint
from Node import Node
import matplotlib.pyplot as plt


class Sudoku:

    #Builds A Sudoku Object, With Corrasponding Components
    def __init__(self, path: str) -> None:
        self.board = self.create(path)  #Board      
        self.create_binary_constraints()  #Constraints
        self.initial_completed = self.get_completed_count() #Count Boxs Known
        self.queue_length = [] 
        self.domain_length = []

    # Creates a Sudoku Board from a .txt file
    def create(self, path: str) -> List[List[Node]]:
        with open(path, "r") as file:
            sudoku = []
            for y, line in enumerate(file):
                row = line.strip().split(",")  #Creates A Node Object For Each Box
                sudoku_row = [Node(x, y, start,self) for x, start in enumerate(row)]
                sudoku.append(sudoku_row)
        return sudoku

    #Creates The Set Of Binary Constraints On The Board
    def create_binary_constraints(self) -> None:
        constraint_index, constraints = set(), list()
        for dim1 in range(9):
            for dim21, dim22 in combinations(range(9), 2):
                constraint_index.add(((dim1, dim21), (dim1, dim22)))  #Row Constraint Index
                constraint_index.add(((dim21, dim1), (dim22, dim1)))  #Column Constraint Index
        for br in range(3):
            for bc in range(3):
                cells = [(3*br+r, 3*bc+d) for r in range(3) for d in range(3)]
                for n1, n2 in combinations(cells, 2):
                    constraint_index.add((n1, n2))  #Box Constraint

        #Moves The Nodes At These Indexs Into List Of Constraints
        for (x1, y1), (x2, y2) in sorted(list(constraint_index)):
            N1, N2 = self.board[y1][x1], self.board[y2][x2]
            constraints.append(Constraint(N1, N2))
            constraints.append(Constraint(N2, N1))
        self.constraints = constraints #Sets Board Total Constraints

        #Stores List Of Constraints Connected to each Node
        for row in self.board: 
            for node in row: node.set_constraints(self.constraints)

    #Returns the number of completed boxs
    def get_completed_count(self) -> int:
        return sum(1 for row in self.board for node in row if len(node.domain) == 1)

    #Returns Whether Sudoku is completed
    def is_solved(self) -> bool:
        return self.get_completed_count() == 81







    
    #Completes The AC_3 Algorithm To Create Arc Consistency
    def AC_3(self) -> Optional[bool]:
        queue, queue_set = deque(self.constraints), set(self.constraints)
        while queue:
            self.queue_length.append(len(queue_set)) #Mark Queue Length At This Step
            #self.domain_length.append(sum([len(node.domain) for node for row in self.board]))

            self.domain_length.append(sum(len(node.domain) for row in self.board for node in row))



            constraint = queue.popleft()
            queue_set.remove(constraint)
            if constraint.revise():  #If domain has been changed
                if len(constraint.node1.domain) == 0:
                    return None  #No domain, meaning no solution
                else:
                    #Otherwise add all neighbours who might be changed due to this
                    for neighbour_constraint in constraint.node1.constraints:
                        if neighbour_constraint not in queue_set:
                            queue.append(neighbour_constraint)
                            queue_set.add(neighbour_constraint)
        return self.is_solved()

    #Completes a Backtracking Algorithm To Reduce Domains
    def BTS(self) -> Optional[bool]:
        # Select a variable (node) with the smallest domain > 1 (MRV heuristic)
        node = min((node for row in self.board for node in row if len(node.domain) > 1),
            key=lambda n: len(n.domain), default=None,)
            
        if node is None: return True  #All Assigned

        # Iterate over a copy of the domain to try each possible value
        original_domain = node.domain.copy()
        for value in original_domain:
            if node.is_consistent(value):
                node.set_value(value)  # Assign the value
                if self.BTS():
                    return True
                node.reset_value()  # Reset if backtracking occurs
        return None

    #Solves A Sudoku Board Using AC_3 and Backtracking Search Algorithm
    def solve(self, distinguish_initial = False, plot=False) -> None:

        #Already Solved
        if self.is_solved(): print("Already Solved:")
        #Not Solved
        else:
            print(f"Starting:    {self.initial_completed}")
            AC_3_result = self.AC_3()

            #If Failed To Make Consistent
            if AC_3_result == None: print("After AC_3:  Invalid Puzzle Discovered")
            #If Solved
            elif AC_3_result == True: print("After AC_3:  81 - Solved")

            #If Partially Solved
            else:
                print(f"After AC_3:  {self.get_completed_count()}")
                BTS_result = self.BTS()

                #If Failed To Reduce Domain
                if BTS_result == None: print("After AC_3:   Invalid Puzzle Discovered")
                #Succeeded
                else: print("After BTS:   81 - Solved")
        self.print_board(distinguish_initial)
        if plot: self.plot_AC_3()


    #Prints A Copy Of The Boards Current State
    def print_board(self, distinguish_initial = False) -> None:
        print(f"Completed(Initial): {self.get_completed_count()}/81({self.initial_completed})")
        for row in self.board:
            print(",".join([node.get_state(distinguish_initial) for node in row]))

        
    def plot_AC_3(self):
        plt.plot(self.queue_length, marker='o', color='red')
        plt.plot(self.domain_length, marker='*', color='blue')
        plt.xlabel("Iteration")
        plt.ylabel("Queue(red) / Domain (blue) length")
        plt.title("Size Of Queue(red) and Size Of Domain(blue) at Iteration Of AC-3")
        plt.grid(True)
        plt.show()
        
