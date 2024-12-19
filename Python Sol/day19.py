lines = open("day19.txt").read().strip()
lines = lines.split('\n\n')

towels = [i.strip() for i in lines[0].split(",")]
design = [i for i in lines[1].split('\n')]

def create_design(design, towels):

    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for towel in towels:
            towel_len = len(towel)
            if (i >= towel_len and 
                dp[i - towel_len] and 
                design[i - towel_len:i] == towel):
                dp[i] = True
                break
    
    return dp[n]

possible = [False] * len(design)
res = 0
for i, d in enumerate(design):
    if create_design(d, towels):
        possible[i] = True
        res += 1

print(f"Part 1: {res}")

##########################
######### Part 2 #########
##########################

memo = {}

def count_design(design, towels, pos=0):
    if pos == len(design):
        return 1
    
    key = design[pos:]
    if key in memo:
        return memo[key]
    
    ways = 0
    for t in towels:
        t = t.strip()
        if (pos + len(t) <= len(design) and 
            design[pos:pos+len(t)] == t):
            ways += count_design(design, towels, pos + len(t))
    
    memo[key] = ways
    return ways

res = 0
for i, d in enumerate(design):
    if possible[i]:
        res += count_design(d, towels)

print(f"Part 2: {res}") 


       
       
