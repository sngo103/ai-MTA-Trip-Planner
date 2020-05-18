# Anton Goretsky
# board_structure.py
# CSCI 350 Assignment 1
# The file containing the main classes used in Assignment 1, Q1

# A class created specifically for the PriorityQueue,
# in order to manage tie breakers in a PQ structure.
class board_tuple:
    
    # Default Constructor.
    # Consists of priority queue value and the board_state class.
    def __init__(self, priority, board):
        self.priority = priority
        self.board = board

    # Equality function, returns if priorities are equal.
    def __eq__(self, input_board):
        return self.priority == input_board.priority

    # Comparison function. Bases on priority first, if equal, bases on directional priority.
    def __lt__(self, input_board_tuple):
        if self.priority != input_board_tuple.priority:
            return self.priority < input_board_tuple.priority
        
        if self.board.past_dir == "Up":
            compare_self = 1
        elif self.board.past_dir == "Down":
            compare_self = 2
        elif self.board.past_dir == "Left":
            compare_self = 3
        else:
            compare_self = 4
        
        if input_board_tuple.board.past_dir == "Up":
            compare_other = 1
        elif input_board_tuple.board.past_dir == "Down":
            compare_other = 2
        elif input_board_tuple.board.past_dir == "Left":
            compare_other = 3
        else:
            compare_other = 4

        return compare_self < compare_other


# The standard board class.
class board_state:

    # Constructor, default where input_board == None and otherwise.
    # Expands input string into an actual 2d array
    def __init__(self, input_board = None):
        #print('Inside Init')
        if input_board == None:
            #print("New Empty Board Constructor")
            self.configuration = []
            self.parent = None
            self.past_dir = ""
            self.root_row = -1
            self.root_col = -1
            self.depth = 0

        else:
            #print("In else section")
            # Set defaults
            self.configuration = []
            self.parent = None
            self.past_dir = ""
            self.root_row = 0
            self.root_col = 0
            self.depth = 0

            # Expand input into configuration
            board_nums_list = [ int(num) for num in input_board.split(',') ]
            board_nums_preprocess = [board_nums_list[i:i + 3] for i in range(0, 9, 3)]
            self.configuration = board_nums_preprocess
            self.root_row = self.find(0)[0]
            self.root_col = self.find(0)[1]

    # Function that copies that input board to self.
    def copy(self, input_board):
        self.root_row = input_board.root_row
        self.root_col = input_board.root_col
        self.depth = input_board.depth
        self.parent = input_board
        self.configuration = [x[:] for x in input_board.configuration]
        # Past Dir will be set during neighbor creation outside of of copy function.

    # Equality checking function, checks if boards are the same.
    def __eq__(self, input_board):
        #print("You callin?")
        #**#print(self.configuration == input_board.configuration)
        return (self.configuration == input_board.configuration)

    # Hash is equivalent to a tostring() function.
    # Necessary for python's implementation of certain classes.
    def __hash__(self):
        return hash(str(self.configuration))
    
    # Function to determine if at goal state.
    def goal_test(self):
        goal = [[0,1,2],[3,4,5],[6,7,8]]
        return self.configuration == goal
    
    # Function to find the [row][col] indexes of a given value in the board.
    def find(self, input_value):
        for row in range(3):
            for col in range(3):
                if self.configuration[row][col] == input_value:
                    return (row,col)
        return (-1,-1)

    # Function to have a string represntation of board configuration for easy printing purposes.
    def __str__(self):
        output = "[\n"
        for row in self.configuration:
            output += str(row) + '\n'
        output += "]"
        return output
        
    # Function to generate the neighbor to self in the given direction.
    # Returns if direction is valid or not valid, modifies caller with direction changes if valid.
    def find_neighbor(self, direction):

        if direction == "Up":
            if self.root_row == 0:
                return False
            else:
                item = self.configuration[self.root_row-1][self.root_col]
                self.configuration[self.root_row-1][self.root_col] = 0
                self.configuration[self.root_row][self.root_col] = item
                self.root_row -= 1
                self.past_dir = "Up"
                return True
        elif direction == "Down":
            if self.root_row == 2:
                return False
            else:
                item = self.configuration[self.root_row+1][self.root_col]
                self.configuration[self.root_row+1][self.root_col] = 0
                self.configuration[self.root_row][self.root_col] = item
                self.root_row += 1
                self.past_dir = "Down"
                return True
        elif direction == "Left":
            if self.root_col == 0:
                return False
            else:
                item = self.configuration[self.root_row][self.root_col-1]
                self.configuration[self.root_row][self.root_col-1] = 0
                self.configuration[self.root_row][self.root_col] = item
                self.root_col -= 1
                self.past_dir = "Left"
                return True
        elif direction == "Right":
            if self.root_col == 2:
                return False
            else:
                item = self.configuration[self.root_row][self.root_col+1]
                self.configuration[self.root_row][self.root_col+1] = 0
                self.configuration[self.root_row][self.root_col] = item
                self.root_col += 1
                self.past_dir = "Right"
                return True

        return False

    # Heuristic function for A*
    # Goal board is passed as input to avoid regeneration each time heuristic is called.
    def heuristic(self, goal_board):
        output = 0
        for row_ind in range(3):
            for col_ind in range(3):
                if self.configuration[row_ind][col_ind] == 0:
                    pass
                else:
                    coords = goal_board.find(self.configuration[row_ind][col_ind])
                    output += abs(coords[0] - row_ind) + abs(coords[1] - col_ind)
        return self.depth + output
