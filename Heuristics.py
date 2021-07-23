import TileProblem


def H1(tileArray, size:int): # Manhattan Heuristic
    solvedTile = TileProblem.solveTile(size)
    HArray = [[0 for x in range(size)] for y in range(size)]
    for row in range(size):
        for col in range(size):
            pos = expectedPosition(solvedTile, tileArray[row][col], size)
            HArray[row][col] = abs(pos[0] - row) + abs(pos[1] - col)
    return HArray


# Returns the expected position of a given value in the solved tile
def expectedPosition(solvedTile, value, size):
    for row in range(size):
        for col in range(size):
            if solvedTile[row][col] == value:
                return [row, col]
    return [0, 0]


def H2(tileArray, size:int): # Number of displaced tiles Heuristic
    solvedTile = TileProblem.solveTile(size)
    HArray = [[0 for x in range(size)] for y in range(size)]
    for row in range(size):
        for col in range(size):
            if tileArray[row][col] != solvedTile[row][col]:
                HArray[row][col] = 1
            else:
                HArray[row][col] = 0
    return HArray


# This is really the goal testing that was meant to be handles in TileProblem
# It returns a totalCost of the given Heuristic, which is then handled in puzzleSolver
# If the total cost is zero, that means we've reached the goal state.
def totalCost(heuristic, size:int):
    cost = 0
    for row in range(size):
        for col in range(size):
            cost += heuristic[row][col]
    return cost
