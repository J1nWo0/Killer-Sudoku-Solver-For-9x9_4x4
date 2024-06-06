import pulp

class KillerSudokuSolver:
    def __init__(self, grid_size, cage_constraints):
        highest_sum = max(constraint["sum"] for constraint in cage_constraints)
        size = 9 if highest_sum > 10 else 4


        self.grid_size = size  # Size of the Sudoku grid (e.g., 4x4, 9x9)
        self.cage_constraints = cage_constraints  # List of cage constraints, each with a sum and a list of cells
        self.distinct_groups = self._generate_distinct_groups()  # Generate the distinct groups for rows, columns, and boxes
        

    def _generate_distinct_groups(self):
        # Create row groups: each row is a group of cells
        row_groups = [[(i, j) for j in range(self.grid_size)] for i in range(self.grid_size)]
        
        # Create column groups: each column is a group of cells
        col_groups = [[(j, i) for j in range(self.grid_size)] for i in range(self.grid_size)]
        
        # Calculate the size of each box (e.g., 3x3 in a 9x9 grid)
        box_size = int(self.grid_size ** 0.5)
        
        # Create box groups: each box is a group of cells
        box_groups = [
            [(box_size * i + k, box_size * j + l) for k in range(box_size) for l in range(box_size)]
            for i in range(box_size)
            for j in range(box_size)
        ]
        
        # Return the combined list of row, column, and box groups
        return row_groups + col_groups + box_groups

    def solve(self):
        # Define the optimization problem (minimization with an arbitrary objective)
        prob = pulp.LpProblem("Killer_Sudoku_Problem_KA", pulp.LpMinimize)
        prob += 0, "Arbitrary Objective Function"

        # Create binary decision variables for choices (i, j, n) where i and j are cell indices, n is a number
        choices = pulp.LpVariable.dicts(
            "choices", (range(self.grid_size), range(self.grid_size), range(1, self.grid_size + 1)), cat="Binary"
        )

        # Constraint: Each cell must contain exactly one number
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                prob += pulp.lpSum([choices[i][j][n] for n in range(1, self.grid_size + 1)]) == 1

        # Constraint: Each number must appear exactly once in each row, column, and box
        for n in range(1, self.grid_size + 1):
            for distinct_group in self.distinct_groups:
                prob += pulp.lpSum([choices[i][j][n] for i, j in distinct_group]) == 1

        # Constraint: Sum of the numbers in each cage must equal the specified cage total
        for constraint in self.cage_constraints:
            target_sum = constraint["sum"]
            cells = constraint["cells"]
            prob += pulp.lpSum([choices[i][j][n] * n for i, j in cells for n in range(1, self.grid_size + 1)]) == target_sum

        # Solve the problem
        prob.solve()

        # Print the status of the solution (Optimal, Infeasible, etc.)
        print('Status:', pulp.LpStatus[prob.status])
        
        # Extract the solution: Create a grid with the solved values
        result = [
            [sum([choices[i][j][n].varValue * n for n in range(1, self.grid_size + 1)]) for j in range(self.grid_size)]
            for i in range(self.grid_size)
        ]

        result = self.convert_to_int_or_float(result)

        # Return the solution if it is optimal, otherwise return None
        if pulp.LpStatus[prob.status] == 'Optimal':
            return result
        else:
            return None
        
    def convert_to_int_or_float(self, array):
        # Convert the float values in the result to integers if they are whole numbers
        def convert_value(val):
            if val.is_integer():
                return int(val)
            else:
                return val
        
        return [[convert_value(val) for val in sublist] for sublist in array]

def check_missing_coordinates(size, cage_constraints):
    # Create a set of all coordinates in the grid
    all_coordinates = {(i, j) for i in range(size) for j in range(size)}
    used_coordinates = set()  # Track coordinates used in cages
    cage_coordinates = []
    
    for cage in cage_constraints:
        cage_set = set()
        for cell in cage["cells"]:
            # Check for duplicate coordinates across cages
            if cell in used_coordinates:
                print(f"Warning: Coordinate {cell} is duplicated across multiple cages")
                return True
            # Check if cell coordinates are out of bounds
            if not (0 <= cell[0] < size and 0 <= cell[1] < size):
                print(f"Warning: Coordinate {cell} is out of bounds for {size}x{size} Sudoku")
                return True
            cage_set.add(cell)
            used_coordinates.add(cell)  # Mark the coordinate as used
        cage_coordinates.append(cage_set)
    
    # Check for any missing coordinates (not covered by cages)
    all_cage_coordinates = set().union(*cage_coordinates)
    missing_coordinates = all_coordinates - all_cage_coordinates
    if missing_coordinates:
        print(f"Warning: Missing coordinates for {size}x{size} Killer Sudoku:", missing_coordinates)
    return bool(missing_coordinates)

# Example 4x4 Killer Sudoku
cage_constraints = [
    {"sum": 6, "cells": [(0,0),(1,0)]},
    {"sum": 8, "cells": [(0,1),(0,2),(0,3)]},
    {"sum": 5, "cells": [(1,1),(2,1)]},
    {"sum": 6, "cells": [(1,2),(2,2)]},
    {"sum": 4, "cells": [(1,3),(2,3)]},
    {"sum": 8, "cells": [(2,0),(3,0),(3,1)]},
    {"sum": 3, "cells": [(3,2),(3,3)]}
]

# Example 9x9 Killer Sudoku
# cage_constraints = [
#     {"sum":  6, "cells": [(0,0)]},
#     {"sum": 28, "cells": [(0,1), (0,2), (1,0), (1,1)]},
#     {"sum": 19, "cells": [(0,3), (0,4), (1,2), (1,3), (1,4)]},
#     {"sum": 15, "cells": [(0,5), (0,6), (0,7)]},
#     {"sum":  7, "cells": [(0,8)]},
#     {"sum": 11, "cells": [(1,5), (2,5)]},
#     {"sum": 18, "cells": [(1,6), (2,6), (3,6)]},
#     {"sum": 19, "cells": [(1,7), (1,8), (2,7), (3,7)]},
#     {"sum": 14, "cells": [(2,0), (3,0)]},
#     {"sum":  4, "cells": [(2,1), (2,2)]},
#     {"sum":  9, "cells": [(2,3), (2,4)]},
#     {"sum":  4, "cells": [(2,8)]},
#     {"sum":  7, "cells": [(3,1), (4,1)]},
#     {"sum": 19, "cells": [(3,2), (3,3), (4,2)]},
#     {"sum":  5, "cells": [(3,4), (3,5)]},
#     {"sum": 17, "cells": [(3,8), (4,8)]},
#     {"sum": 17, "cells": [(4,0), (5,0), (6,0), (7,0), (8,0)]},
#     {"sum":  9, "cells": [(4,3), (4,4)]},
#     {"sum": 13, "cells": [(4,5), (4,6), (4,7)]},
#     {"sum": 19, "cells": [(5,1), (6,1), (6,2)]},
#     {"sum": 17, "cells": [(5,2), (5,3), (5,4)]},
#     {"sum": 14, "cells": [(5,5), (5,6)]},
#     {"sum":  9, "cells": [(5,7), (5,8), (6,8)]},
#     {"sum": 12, "cells": [(6,3), (6,4)]},
#     {"sum": 19, "cells": [(6,5), (6,6), (6,7), (7,6)]},
#     {"sum": 15, "cells": [(7,1), (7,2), (7,3)]},
#     {"sum": 12, "cells": [(7,4), (7,5)]},
#     {"sum": 13, "cells": [(7,7), (8,7)]},
#     {"sum": 11, "cells": [(7,8), (8,8)]},
#     {"sum":  8, "cells": [(8,1), (8,2)]},
#     {"sum": 12, "cells": [(8,3), (8,4)]},
#     {"sum":  3, "cells": [(8,5), (8,6)]},
# ]

if __name__ == "__main__":
    # Determine grid size based on the highest cage sum
    highest_sum = max(constraint["sum"] for constraint in cage_constraints)
    size = 9 if highest_sum > 10 else 4
    
    # Check for any missing or duplicated coordinates in cage constraints
    missing_coordinates_exist = check_missing_coordinates(size, cage_constraints)

    if missing_coordinates_exist:
        print("No solution exists.")
    else:
        print(f"Solving {size}x{size} Killer Sudoku:\n")
        killer_sudoku = KillerSudokuSolver(size, cage_constraints)
        solution = killer_sudoku.solve()
        if solution:
            print(solution)
            print(f"{size}x{size} Killer Sudoku Solution:")
            for row in solution:
                print(row)
        else:
            print("No solution exists.")
