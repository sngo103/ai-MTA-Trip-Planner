# Anton Goretsky
# driver.py
# CSCI 350 Assignment 1
# The main driver file for Assignent 1, Q1

import sys
from collections import deque
from queue import PriorityQueue
import heapq
import time
import resource
import board_structure

# Path Function
# Traces the output path via parent board classes, stored under [boardobject].parent
def path(start, end):
    output = []
    while end != start:
        output = [end.past_dir] + output
        end = end.parent
    return output

# Breadth-First Search
# Follows the implementation from textbook directly, using a deque, 
# but implementing it as a regular queue.
def bfs(input_board):
    frontier = deque()
    frontier.append(input_board)
    
    explored = set()
    expanded = 0
    max_search_depth = 0
    while frontier:
        new = frontier.popleft()
        explored.add(new)

        if new.goal_test():
            return expanded, max_search_depth, new

        expanded += 1
        neighbor_dirs = ["Up", "Down", "Left", "Right"]
        
        for direc in neighbor_dirs:
            neighbor_temp = board_structure.board_state()
            neighbor_temp.copy(new)
            neighbor_temp.depth += 1
            worked = neighbor_temp.find_neighbor(direc)
            if worked and neighbor_temp not in explored:
                frontier.append(neighbor_temp)
                # This solution will reduce complexity to O(1) from O(n) of usual union section
                # Changes functionality slightly of explored, but not needed in this implementation to be strict.
                explored.add(neighbor_temp)
                max_search_depth = max(max_search_depth, neighbor_temp.depth)

    print("Impossible or Something Broke...")
    return None, None, None

# Depth-First Search
# Follows the implementation from textbook directly, using a list, 
# but implementing it as a stack.
def dfs(input_board):
    frontier = []
    frontier.append(input_board)
    
    explored = set()
    expanded = 0
    max_search_depth = 0
    while frontier:
        new = frontier.pop()
        explored.add(new)

        if new.goal_test():
            return expanded, max_search_depth, new

        expanded += 1
        neighbor_dirs = ["Right", "Left", "Down", "Up"]
        
        for direc in neighbor_dirs:
            neighbor_temp = board_structure.board_state()
            neighbor_temp.copy(new)
            neighbor_temp.depth += 1
            worked = neighbor_temp.find_neighbor(direc)
            if worked and neighbor_temp not in explored:
                frontier.append(neighbor_temp)
                # This solution will reduce complexity to O(1) from O(n) of usual union section
                # Changes functionality slightly of explored, but not needed in this implementation to be strict.
                explored.add(neighbor_temp)
                max_search_depth = max(max_search_depth, neighbor_temp.depth)

    print("Impossible or Something Broke...")
    return None, None, None

# A-Star Search
# Follows the implementation from textbook directly, using a PriorityQueue
# Uses a new board_tuple class due to __lt__ method necessary with priority and data point.
def ast(input_board):
    input_board_tuple = board_structure.board_tuple(0, input_board)

    # Generate goal board for heuristic function use
    goal_board = board_structure.board_state("0,1,2,3,4,5,6,7,8")
    
    # Initialization
    frontier = PriorityQueue()
    frontier.put(input_board_tuple)
    explored = set()
    expanded = 0
    max_search_depth = 0

    while not frontier.empty():

        new = frontier.get()
        explored.add(new.board)

        if new.board.goal_test():
            return expanded, max_search_depth, new.board

        expanded += 1
        neighbor_dirs = ["Up", "Down", "Left", "Right"]
        
        for direc in neighbor_dirs:
            neighbor_temp = board_structure.board_state()
            neighbor_temp.copy(new.board)
            neighbor_temp.depth += 1
            worked = neighbor_temp.find_neighbor(direc)
            if worked and neighbor_temp not in explored:
                # Heuristic Function
                # Note: Key decrease if in frontier is not necessary, due to __lt__ in board_tuple class.
                hn = neighbor_temp.heuristic(goal_board)
                neighbor_temp_tuple = board_structure.board_tuple(hn, neighbor_temp)
                frontier.put(neighbor_temp_tuple)
                # This solution will reduce complexity to O(1) from O(n) of usual union section
                # Changes functionality slightly of explored, but not needed in this implementation to be strict.
                explored.add(neighbor_temp)
                max_search_depth = max(max_search_depth, neighbor_temp.depth)

    print("Impossible or Something Broke...")
    return None, None, None

# Main driver function
def main():

    # Pull out arguments
    input_args = sys.argv
    search_type = input_args[1]
    board_nums = input_args[2]
    initial_board = board_structure.board_state(board_nums)
    
    # Call respective search
    if search_type == "bfs":
        start = time.time()
        expanded_nodes, max_search_depth, end_board = bfs(initial_board)
        path_list = path(initial_board, end_board)
        end = time.time()
    
    elif search_type == "dfs":
        start = time.time()
        expanded_nodes, max_search_depth, end_board = dfs(initial_board)
        path_list = path(initial_board, end_board)
        end = time.time()

    elif search_type == "ast":
        start = time.time()
        expanded_nodes, max_search_depth, end_board = ast(initial_board)
        path_list = path(initial_board, end_board)
        end = time.time()

    else:
        print("INVALID SEARCH TYPE INPUT")
    # Get RAM usage
    RAM = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # Print output
    #print("path_to_goal: " + str(path_list))
    #print("cost_of_path: " + str(len(path_list)))
    #print("nodes_expanded: " + str(expanded_nodes))
    #print("search_depth: " + str(len(path_list)))
    #print("max_search_depth: " + str(max_search_depth))
    #print("running_time: " + format(end - start, '.8f'))
    #print("max_ram_usage: " + format(RAM * 0.0000001, '.8f'))

    # Write to output file
    f = open("output.txt", 'w')
    f.write("path_to_goal: " + str(path_list))
    f.write("\ncost_of_path: " + str(len(path_list)))
    f.write("\nnodes_expanded: " + str(expanded_nodes))
    f.write("\nsearch_depth: " + str(len(path_list)))
    f.write("\nmax_search_depth: " + str(max_search_depth))
    f.write("\nrunning_time: " + format(end - start, '.8f'))
    f.write("\nmax_ram_usage: " + format(RAM * 0.0000001, '.8f'))
    f.close()

    # For good measure :)
    return 0

if __name__== "__main__":
  main()
