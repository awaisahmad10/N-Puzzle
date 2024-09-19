from copy import deepcopy
import math

#get k value from user, making sure 3 <= k <= 5
while True:
    k = int(input())
    if (k >= 3) and (k <= 5):
        break

#initialize given grid and target grid
grid = []
goal_grid = []
i = 0

# build the k*k grids using nested for loops and users input
for x in range(k):
    row = []
    goal_row = []
    for y in range(k):
        cell = int(input())
        if cell == 0:
            cell0_location = (x, y)
        row.append(cell)
        goal_row.append(i)
        i += 1
    grid.append(row)
    goal_grid.append(goal_row)

#define possible moves for 'empty' cell based on its position on the grid
def moves(cell0_location):
    possibleMoves = []
    if cell0_location[0] > 0: 
        possibleMoves.append('UP')
    if cell0_location[0] < k-1: 
        possibleMoves.append('DOWN')
    if cell0_location[1] > 0: 
        possibleMoves.append('LEFT')
    if cell0_location[1] < k-1: 
        possibleMoves.append('RIGHT')
    return possibleMoves

#calculate the total manhattan distance using L1/ Cityblock method
def manhattanDistance(grid1):
    manhattan_distance = 0
    for i in range(k):
        for x in range(k):
            manhattan_distance += abs(math.floor(grid1[i][x]/3) - i) + abs((grid1[i][x]%k)-x)
    return manhattan_distance

#change the grid based on the current state of the grid, direction, and current location of empty cell
def changeGrid(current_grid, move_made, cell0_location):
    #create copy of grid to manipulate
    new_grid = deepcopy(current_grid)
    #if the direction of the move is UP, change the x/ row to be -1 its value
    # and so on for the other directions...
    if move_made == "UP":
        shift = new_grid[cell0_location[0]-1][cell0_location[1]]
        new_grid[cell0_location[0]][cell0_location[1]] = shift
        new_grid[cell0_location[0]-1][cell0_location[1]] = 0
    if move_made == "DOWN":
        shift = new_grid[cell0_location[0]+1][cell0_location[1]]
        new_grid[cell0_location[0]][cell0_location[1]] = shift
        new_grid[cell0_location[0]+1][cell0_location[1]] = 0
    if move_made == "LEFT":
        shift = new_grid[cell0_location[0]][cell0_location[1]-1]
        new_grid[cell0_location[0]][cell0_location[1]] = shift
        new_grid[cell0_location[0]][cell0_location[1]-1] = 0
    if move_made == "RIGHT":
        shift = new_grid[cell0_location[0]][cell0_location[1]+1]
        new_grid[cell0_location[0]][cell0_location[1]] = shift
        new_grid[cell0_location[0]][cell0_location[1]+1] = 0
    #return the grid after moving the empty cell
    return new_grid

#initialize a hash baord to keep track of visited states of grid
def hashGrid(grid):
    string_grid = ''
    for r in range(k):
        for c in range(k):
            string_grid += str(grid[r][c])
    return string_grid

#create the prority queue of grids (branches) to be checked by comparing the f(x) values to the current lowest value in the frontier list
def priorityQueue(parent):
    low=0
    high=len(frontier_list)
    while low < high:
        mid = (low+high) // 2
        if parent[5] < frontier_list[mid][5]: 
            low = mid+1
        else: 
            high = mid
    frontier_list.insert(low, parent)

# create the branches in the tree from the parent node/ grid
def branches(parent):
    #get needed information from parent node (current state of grid, coordinates of empty cell, g(x) value...)
    current_grid = parent[0]
    cell0_location = parent[1]
    g_value = parent[3] + 1

    #for all possible moves on the current empty cell location,
    #calculate the h(x) value and move the empty cell in that direction
    for move in moves(cell0_location):
        temp = deepcopy(current_grid)
        if move == "UP":
            h_value = manhattanDistance(changeGrid(temp, "UP", cell0_location))
            M = "UP"
            new_cell0_location = (cell0_location[0]-1, cell0_location[1])
        elif move == "DOWN":
            h_value = manhattanDistance(changeGrid(temp, "DOWN", cell0_location))
            M = "DOWN"
            new_cell0_location = (cell0_location[0]+1, cell0_location[1])
        elif move == "LEFT":
            h_value = manhattanDistance(changeGrid(temp, "LEFT", cell0_location))
            M = "LEFT"
            new_cell0_location = (cell0_location[0], cell0_location[1]-1)
        elif move == "RIGHT":
            h_value = manhattanDistance(changeGrid(temp, "RIGHT", cell0_location))
            M = "RIGHT"
            new_cell0_location = (cell0_location[0], cell0_location[1]+1)

        #change the grid from the given move and create the hash grid
        new_grid = changeGrid(temp, M, cell0_location)
        hash = hashGrid(new_grid)

        #check if the hash grid has not been visited yet
        #if not, the calculate the f(x) value from the given h(x) and g(x) values 
        #and add it to the priority queue and visited grids
        if hash not in visited_grids:
            f_value = g_value + h_value
            priorityQueue((new_grid, new_cell0_location, M, g_value, h_value, f_value, parent))
            visited_grids.add(hash)

#initialzie a set to keep track of all visited grids
visited_grids = set()
visited_grids.add(hashGrid(grid))

#calculate the heuristic h(x) value for the given grid
man_dist = manhattanDistance(grid)
#initialize the g(x) value and frontier list
cost_so_far = 0
frontier_list = []
#add the given grid to the frontier list and 'START' solving
frontier_list.append((grid, cell0_location, "START", cost_so_far, man_dist, man_dist + cost_so_far, None))

#initalize a list to keep track of the moves made so far
moves_made = []
while True:
    #if the manhattan distance for the grid is 0, then the grid is solved
    parent = frontier_list.pop()
    if parent[4] == 0:
        grid_solved = parent
        break
    #otherwise keep generating the branches to search
    branches(parent)

parent = grid_solved
while parent is not None:
    #append all the moves made to get to the solution to the list
    moves_made.append(parent[2])
    parent = parent[6]

#reverse the order of the list to display them correctly
moves_made = moves_made[::-1]

#print the number of moves made to solve the puzzle and what they were
print(len(moves_made) - 1)
for move in range(1, len(moves_made)):
    print(moves_made[move])
