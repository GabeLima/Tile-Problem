import math


# Generate a solved tile, use this in creating the Heuristics
def solveTile(size:int):
    solvedTile = [[0 for x in range(size)] for y in range(size)]
    for i in range(size):
        for j in range(size):
            solvedTile[i][j] = i * size + j + 1# Place each number in its corresponding place
    solvedTile[size-1][size-1] = 0 # This indicates where the blank space is going to be at the end
    return solvedTile


# Construct a tileArray based off a given string (comes from the file, the string comes from puzzleSovler)
def constructInstance(fileText: str):
    fileText.replace('\n', ',')
    fileText.replace('\t', '')
    # print(fileText)
    tileArray = fileText.split(',')
    if tileArray[-1] == "'":
        del tileArray[len(tileArray) - 1:]
    print("Tile Array '%s'" % tileArray)
    max = 0
    for nums in tileArray:
        if nums.isdigit():
            if int(nums) > max:
                max = int(nums)

    max += 1
    size = int(math.sqrt(max))
    inputTile = [[0 for x in range(size)] for x in range(size)]
    for row in range(size):
        for col in range(size):
            if tileArray[row * size + col].isdigit():
                inputTile[row][col] = int(tileArray[row * size + col])
            else:
                inputTile[row][col] = 0
    print("Input tile: %s" % inputTile)
    return inputTile
