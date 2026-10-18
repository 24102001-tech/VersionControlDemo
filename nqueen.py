import heapq

class BoardState:
    def __init__(self, queens, n):
        self.queens = queens  # List mapping column index -> row index
        self.n = n
        self.g = len(queens)  # Cost to reach this node (number of placed queens)
        self.h = self.calculate_heuristic()
        self.f = self.g + self.h

    def calculate_heuristic(self):
        """Counts the number of mutually attacking queen pairs on the board."""
        conflicts = 0
        num_queens = len(self.queens)
        
        for i in range(num_queens):
            for j in range(i + 1, num_queens):
                # Same row conflict
                if self.queens[i] == self.queens[j]:
                    conflicts += 1
                # Diagonal conflicts (slope delta_row / delta_col == 1 or -1)
                elif abs(self.queens[i] - self.queens[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    # Defining comparison operations for the Priority Queue (heapq)
    def __lt__(self, other):
        return self.f < other.f

def solve_n_queens_astar(n):
    # Min-priority queue initialized with an empty board state
    open_set = []
    initial_state = BoardState([], n)
    heapq.heappush(open_set, initial_state)
    
    nodes_expanded = 0

    while open_set:
        current_state = heapq.heappop(open_set)
        nodes_expanded += 1

        # Goal check: All queens are placed and there are zero conflicts
        if len(current_state.queens) == n and current_state.h == 0:
            return current_state.queens, nodes_expanded

        # Generate next states by trying to place a queen in the next available column
        next_col = len(current_state.queens)
        if next_col < n:
            for next_row in range(n):
                new_queens = current_state.queens + [next_row]
                child_state = BoardState(new_queens, n)
                
                # Pruning optimization: Only push states where the newest queen 
                # does not instantly cause a deadlock conflict with previous queens.
                if child_state.h == current_state.h:  
                    heapq.heappush(open_set, child_state)
                    
    return None, nodes_expanded

def print_board(queens_config, n):
    """Utility function to render the chessboard configuration visually."""
    if not queens_config:
        print("No solution found.")
        return
        
    for row in range(n):
        row_str = ""
        for col in range(n):
            if queens_config[col] == row:
                row_str += " Q "
            else:
                row_str += " . "
        print(row_str)

# Execution Driver
if __name__ == "__main__":
    board_size = 4  # Change this value to scale up (e.g., 8)
    print(f"Solving {board_size}-Queens problem via A* Search...\n")
    
    solution, expanded = solve_n_queens_astar(board_size)
    
    if solution:
        print(f"Solution Found after expanding {expanded} states:")
        print(f"Column Mapping representation: {solution}\n")
        print_board(solution, board_size)
    else:
        print("No solution exists for this configuration.")
