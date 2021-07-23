import sys
import Heuristics
import TileProblem
import time

exploredStates = 0
maxDepth = 0


# Swap a row and a column with a given direction (U, D, L, R). It's assumed that the input direction is correct
# but it still accounts for various cases
def swap(row, col, oldMatrix, direction):
    horizontal = 0
    vertical = 0
    if direction == 1:
        vertical = -1
    elif direction == 2:
        horizontal = 1
    elif direction == 3:
        vertical = 1
    elif direction == 4:
        horizontal = -1
    else:
        print("ERROR")
        return oldMatrix
    size = len(oldMatrix)
    matrix = [[0 for x in range(size)] for y in range(size)]
    for newRow in range(size):
        for newCol in range(size):
            matrix[newRow][newCol] = oldMatrix[newRow][newCol]
    if not len(matrix) > row + vertical >= 0 and len(matrix) > col + horizontal >= 0:
        matrix
    temp = matrix[row + vertical][col + horizontal]
    matrix[row + vertical][col + horizontal] = matrix[row][col]
    matrix[row][col] = temp
    return matrix


# Generate the Heuristic we'll be using
def generateH(Matrix, H, size):
    if H == 1:
        return Heuristics.H1(Matrix, size)
    else:
        return Heuristics.H2(Matrix, size)


# Generate and return list of the potential moves we can make from this state in the format
# [[new move matrix, move, state H totalCost, solution String], [...]]
def generateMoves(Matrix, H, size, prevString: str):
    currRow = 0
    currCol = 0
    for row in range(size):
        for col in range(size):
            if Matrix[row][col] == 0:
                currRow = row
                currCol = col
    moveList = []
    if currRow - 1 >= 0:
        if len(prevString) == 0:
            newMatrix = swap(currRow, currCol, Matrix, 1)
            moveList.append([newMatrix, (0, -1), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                      size), prevString + "U"])  # New up state matrix, (0, -1) to represent an up move
        else:
            if prevString[len(prevString) - 1] != 'D':
                newMatrix = swap(currRow, currCol, Matrix, 1)
                moveList.append([newMatrix, (0, -1), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                          size),
                                 prevString + "U"])  # New up state matrix, (0, -1) to represent an up move

    # Right
    if currCol + 1 < size:
        if len(prevString) == 0:
            newMatrix = swap(currRow, currCol, Matrix, 2)
            moveList.append([newMatrix, (1, 0), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                     size), prevString + "R"])  # New right state matrix, (1,0) to represent an right move
        else:
            if prevString[len(prevString) - 1] != 'L':
                newMatrix = swap(currRow, currCol, Matrix, 2)
                moveList.append([newMatrix, (1, 0), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                         size),
                                 prevString + "R"])  # New right state matrix, (1,0) to represent an right move
    # Down
    if currRow + 1 < size:
        if len(prevString) == 0:
            newMatrix = swap(currRow, currCol, Matrix, 3)
            moveList.append([newMatrix, (0, 1), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                     size), prevString + "D"])  # New down state matrix, (0, 1) to represent an down move
        else:
            if prevString[len(prevString) - 1] != 'U':
                newMatrix = swap(currRow, currCol, Matrix, 3)
                moveList.append([newMatrix, (0, 1), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                         size),
                                 prevString + "D"])  # New down state matrix, (0, 1) to represent an down move
    # Left
    if currCol - 1 >= 0:
        if len(prevString) == 0:
            newMatrix = swap(currRow, currCol, Matrix, 4)
            moveList.append([newMatrix, (-1, 0), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                      size), prevString + "L"])  # New right state matrix, (1,0) to represent an right move
        else:
            if prevString[len(prevString) - 1] != 'R':
                newMatrix = swap(currRow, currCol, Matrix, 4)
                moveList.append([newMatrix, (-1, 0), Heuristics.totalCost(generateH(newMatrix, H, size),
                                                                          size),
                                 prevString + "L"])  # New right state matrix, (1,0) to represent an right move
    return moveList


# Pop and remove from the frontier (its assumed that the frontier is sorted beforehand
def pop(frontier):
    front = frontier[0]
    frontier.remove(front)
    return front


# Constructs the Matrix from the given input
def manage_file(inputFile):
    fileObject = open(inputFile, "r")
    text = fileObject.read().replace("\n", " ")
    text = text.replace(' ', ',')
    TileProblem.constructInstance(text)
    return TileProblem.constructInstance(text)


# Returns true if Matrix passed (currentState) is not in the explored list (contains multiple Matrices...)
def explored(currentState, explored):
    if len(explored) == 0:
        explored.append(currentState)
        return False
    else:
        for storedState in explored:
            if currentState == storedState:
                return True
        explored.append(currentState)
    return False


# Sort the frontier by the third value, aka the Heursitic total cost or F value
def sortThird(val):
    return val[2]


# Sorts the frontier
def sortFrontier(frontier):
    # sort the frontier based off the third element in each state
    frontier.sort(key=sortThird, reverse=False)


# A star search solution
# The algorithm behaves as followes:
# Generate and sort a frontier
# While there are still nodes in the frontier, pop the lowest cost state
# If its the solution, return success, else:
# Generate children based off this low cost state, att them to the frontier, and sort it
# Repeat popping, checking, and adding until a solution is found
def AStar(size: int, H: int, inputFile):  # [[new move matrix, move, state H totalCost, solution String], [...]]
    Matrix = manage_file(inputFile)
    exploredList = Matrix
    frontier = generateMoves(Matrix, H, size, "")
    sortFrontier(frontier)
    while not len(frontier) == 0:
        global exploredStates
        exploredStates = exploredStates + 1
        current = pop(frontier)
        if current[2] == 0:
            return current[3] # return the solution string we've been appending to...
        if not explored(current[0], exploredList):
            newMoves = generateMoves(current[0], H, size, current[3])
            for moves in newMoves:
                frontier.append(moves)  # append the new move which is listed above, sort it based off totalCost
            sortFrontier(frontier)


# This is where the recursion for RBFS actually takes place
# Action is an array like this: [new move matrix, move, state H totalCost, solution String]
# The algorithm behaves as follows:
# Generate some children of the current state, sort by the Heuristic, and recursively dive from there.
# If there is an issue (F-Limit or otherwise) return False, indicating a failure
# If all the children return false, the F-Limit needs to be increased
# Keep doing this until a solution is found
def RBFSTwo(Matrix, fLimit, H, size, action, depth):
    global maxDepth
    maxDepth = max(maxDepth, depth)
    if len(action) == 0:
        successors = generateMoves(Matrix, H, size, "")
    else:
        if action[2] == 0:
            return action[3]
        successors = generateMoves(Matrix, H, size, action[3])
    if len(successors) == 0:
        return False
    sortFrontier(successors)
    for move in successors:
        global exploredStates
        exploredStates = exploredStates + 1
        best = move
        if best[2] + depth > fLimit:
            return False
        else:
            result = RBFSTwo(best[0], fLimit, H, size, best, depth + 1)
            if result != False:
                return result
    return False


# See RBFSTwo for an explanation of this function
def RBFS(size: int, H: int, inputFile):
    Matrix = manage_file(inputFile)
    value = False
    fLimit = 10
    while value == False:
        value = RBFSTwo(Matrix, fLimit, H, size, "", 0)
        if isinstance(value, str):
            break
        fLimit = fLimit + 1
        value = False
    return value


def format(input:str):
    newString = ""
    for char in input:
        newString += char + ","
    return newString[:len(newString)-1]


if __name__ == '__main__':
    startTime = time.time()
    A = int(sys.argv[1])  # 1 for A*, 2 for RBFS
    N = int(sys.argv[2])  # size of the puzzle
    H = int(sys.argv[3])  # H = 1 for h1, 2 for h2
    inputFile = sys.argv[4]  # input file
    outputFile = sys.argv[5]  # output file
    if A == 1:
        solutionPath = AStar(N, H, inputFile)
        maxDepth = len(solutionPath)
    else:
        solutionPath = RBFS(N, H, inputFile)
    solutionPath = format(solutionPath)
    f = open(outputFile, "w")
    f.write(solutionPath)
    print(solutionPath)
    endTime = time.time()
    totalTime = str(int(round((endTime * 1000) - (startTime * 1000))))
    print("Time %s" % totalTime)
    print("Explored states %s" % exploredStates)
    print("Depth %s" % maxDepth)
    # print(int(psutil.virtual_memory().total - psutil.virtual_memory().available))
