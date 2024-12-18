from collections import deque
from heapq import heappush, heappop

lines = open("day18.txt").read().strip()
lines = lines.split('\n')

corrupted_bits = [(i.split(",")) for i in lines]
corrupted_bits = [(int(i[0]), int(i[1])) for i in corrupted_bits]

M = 71
N = 71
END = (M-1, N-1)
DIRS = ( (0,1), (1,0), (0,-1), (-1,0) )
memory = [["."] * N for _ in range(M)]

def print_grid(g):
    for row in g:
        print("".join(row))
    print("\n" + "-" * 40)

# Manhattan distance for A*
def heuristic(r, c, ):
    return abs(M-1 - r) + abs(N-1 - c)

def search(limit):
    visited = set()
    h = []
    heappush(h, (0, 0, 0))
    final_cost = 0  

    mem= [["."] * N for _ in range(M)]
    for i, n in enumerate(corrupted_bits):
        if i == limit:
            break
        mem[n[1]][n[0]] = "#"

    while h:
        cost, row, col = heappop(h)

        if (row, col) == END:
            final_cost = cost
            break

        if (row,col) in visited:
            continue
        visited.add((row,col))

        for deltaR, deltaC in DIRS:
            nr, nc = row + deltaR, col + deltaC
            
            if 0 <= nr < M and 0 <= nc < N and mem[nr][nc] != "#" and not (nr,nc) in visited:
                new_cost = cost+1+heuristic(nr, nc)
                heappush(h, (cost+1, nr, nc))
    
    return final_cost

print(f"Part 1: {search(1024)}")

##########################
######### Part 2 #########
##########################

l, r, mid = 0, len(corrupted_bits)-1, 0

while l<=r:
    mid = (l+r)//2
    if search(mid):
        l = mid +1 
    else:
        r = mid -1
        
print(f"Part 2: {str(corrupted_bits[mid-1])[1:-1].replace(' ', '')}")

