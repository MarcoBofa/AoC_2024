from collections import deque
import copy

lines = open("day15.txt").read().strip()
matrix = lines.split('\n')

grid = []
moves = []
robR, robC = 0, 0

i = 0
row = matrix[i]
while "<" not in row and row:
    if "@" in row:
        robR = i
        for j in range(len(row)):
            if row[j] == "@":
                robC = j
    grid.append(list(row))
    i+=1
    row = matrix[i]

i += 1
while i < len(matrix):
    moves.extend(matrix[i])
    i += 1

old_grid = [row.copy() for row in grid]


m = len(grid)
n = len(grid[0])

DIRS = {
    "^": (-1,0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}

def move_robot(r, c, move):
    deltaR, deltaC = DIRS[move]
    nextR, nextC = r + deltaR, c + deltaC

    if grid[nextR][nextC] == "#":
        return r, c
    elif grid[nextR][nextC] == ".":
        grid[r][c] = "."
        grid[nextR][nextC] = "@"
        return nextR, nextC
    else:
        while grid[nextR][nextC] == "O":
            nextR += deltaR
            nextC += deltaC
        if grid[nextR][nextC] == "#":
            return r, c
        elif grid[nextR][nextC] == ".":
            grid[r][c] = "."
            grid[r+deltaR][c+deltaC] = "@"
            grid[nextR][nextC] = "O"
            return r+deltaR, c+deltaC

for move in moves:
    robR, robC = move_robot(robR, robC, move)

gps = 0
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        if val == "O":
            gps += 100 * i + j

print(f"Part 1 result is: {gps}")


##########################
######### Part 2 #########
##########################

def print_grid(g):
    for row in g:
        print("".join(row))
    print("\n" + "-" * 40 + "\n")

new_grid = []

for i, row in enumerate(old_grid):
    nr = []
    for j, val in enumerate(row):
        if val == "#":
            nr.append("#")
            nr.append("#")
        elif val == "O":
            nr.append("[")
            nr.append("]")
        elif val == "@":
            nr.append("@")
            nr.append(".")
        else:
           nr.append(".")
           nr.append(".")

    new_grid.append(nr)

for i, row in enumerate(new_grid):
    for j, val in enumerate(row):
        if val == "@":
            robR = i
            robC = j


# Vertical movement of boxes
def move_boxes(move, g, r, c):
    cp = [row.copy() for row in g]
    deltaR, deltaC = DIRS[move]

    prev = []
    next = []
    prev.append((r,c, "@"))
    cp[r][c] = "."

    while prev:
        for i in prev:
            if g[i[0] + deltaR][i[1]] == "#":
                return g, False
            elif g[i[0] + deltaR][i[1]] == "[":
                next.append((i[0]+deltaR, i[1], "["))
                next.append((i[0]+deltaR,i[1]+1, "]"))

            elif g[i[0] + deltaR][i[1]] == "]":
                next.append((i[0]+deltaR, i[1], "]"))
                next.append((i[0]+deltaR,i[1]-1, "["))
        
        for i in next:
            cp[i[0]][i[1]] = "."
        for i in prev:
            cp[i[0]+deltaR][i[1]] = i[2]
        
        prev = next.copy()
        next = []
    return cp, True


def move_robot2(r, c, move):
    global new_grid
    deltaR, deltaC = DIRS[move]
    nextR, nextC = r + deltaR, c + deltaC

    if new_grid[nextR][nextC] == "#":
        return r, c
    elif new_grid[nextR][nextC] == ".":
        new_grid[r][c] = "."
        new_grid[nextR][nextC] = "@"
        return nextR, nextC
    elif move == ">" or move == "<":
        while new_grid[nextR][nextC] == "[" or new_grid[nextR][nextC] == "]":
            nextR += deltaR
            nextC += deltaC
        if new_grid[nextR][nextC] == "#":
            return r, c
        elif new_grid[nextR][nextC] == ".":
            if move == ">":
                new_grid[r][c+deltaC:nextC+deltaC] = new_grid[r][c:nextC]
                new_grid[r][c] = "."
            else:
                new_grid[r][nextC:c] = new_grid[r][nextC-deltaC:c-deltaC]
                new_grid[r][c] = "."
            return r+deltaR, c+deltaC
    else:
        new_grid, check = move_boxes(move, new_grid, r, c)

        if check:   
            return r+deltaR, c
        else:
            return r,c
            
for move in moves:
    robR, robC = move_robot2(robR, robC, move)

gps = 0
for i, row in enumerate(new_grid):
    for j, val in enumerate(row):
        if val == "[":
            gps += 100 * i + j

print(f"Part 2 result is: {gps}")


# Should comment and improve variable naming, oh well
# Sorry also for the mess :/
