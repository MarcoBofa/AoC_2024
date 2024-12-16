from collections import deque
from heapq import heappush, heappop

lines = open("day16.txt").read().strip()
c = lines.split('\n')
matrix = [list(r) for r in c]

m, n = len(matrix), len(matrix[0])

start = (m-2, 1)
end = (1, n-2)

DIRS = {
    'up':    (-1, 0),
    'right': (0, 1),
    'down':  (1, 0),
    'left':  (0, -1)
}

TURN_LEFT = {
    'up': 'left',
    'left': 'down',
    'down': 'right',
    'right': 'up'
}

TURN_RIGHT = {
    'up': 'right',
    'right': 'down',
    'down': 'left',
    'left': 'up'
}

directions = ['up', 'right', 'down', 'left']

dist = {}
for r in range(m):
    for c in range(n):
        for d in directions:
            dist[(r,c,d)] = float('inf')

dist[(start[0], start[1], 'right')] = 0
pq = []
heappush(pq, (0, start[0], start[1], 'right'))

while pq:
    cost, r, c, direction = heappop(pq)
    if dist[(r,c,direction)] < cost:
        continue

    if (r,c) == end:
        final_cost = cost
        break

    moves = [
        ('straight', direction, 1),
        ('left', TURN_LEFT[direction], 1001),
        ('right', TURN_RIGHT[direction], 1001)
    ]

    for move_type, new_dir, move_cost in moves:
        nr, nc = r + DIRS[new_dir][0], c + DIRS[new_dir][1]
        if matrix[nr][nc] != '#':
            new_cost = cost + move_cost
            if dist[(nr,nc,new_dir)] > new_cost:
                dist[(nr,nc,new_dir)] = new_cost
                heappush(pq, (new_cost, nr, nc, new_dir))


print(f"Part 1 result is: {final_cost}")


##########################
######### Part 2 #########
##########################

end_states = []
for d in directions:
    if dist[(end[0], end[1], d)] == final_cost:
        end_states.append((end[0], end[1], d))

back_visited = set()
queue = deque(end_states)
for st in end_states:
    back_visited.add(st)

used_cells = set()
for (er, ec, ed) in end_states:
    used_cells.add((er,ec))

while queue:
    r, c, d = queue.popleft()
    cur_cost = dist[(r,c,d)]

    for pdir in directions:
        pr = r - DIRS[d][0]
        pc = c - DIRS[d][1]

        if 0 <= pr < m and 0 <= pc < n and matrix[pr][pc] != '#':
            if pdir == d and dist[(pr,pc,pdir)] + 1 == cur_cost:
                if (pr,pc,pdir) not in back_visited:
                    back_visited.add((pr,pc,pdir))
                    queue.append((pr,pc,pdir))
                    used_cells.add((pr,pc))

        if TURN_LEFT[pdir] == d:
            pr = r - DIRS[d][0]
            pc = c - DIRS[d][1]
            if 0 <= pr < m and 0 <= pc < n and matrix[pr][pc] != '#':
                if dist[(pr,pc,pdir)] + 1001 == cur_cost:
                    if (pr,pc,pdir) not in back_visited:
                        back_visited.add((pr,pc,pdir))
                        queue.append((pr,pc,pdir))
                        used_cells.add((pr,pc))

        if TURN_RIGHT[pdir] == d:
            pr = r - DIRS[d][0]
            pc = c - DIRS[d][1]
            if 0 <= pr < m and 0 <= pc < n and matrix[pr][pc] != '#':
                if dist[(pr,pc,pdir)] + 1001 == cur_cost:
                    if (pr,pc,pdir) not in back_visited:
                        back_visited.add((pr,pc,pdir))
                        queue.append((pr,pc,pdir))
                        used_cells.add((pr,pc))

print(f"Part 2 result is: {len(used_cells)}")
