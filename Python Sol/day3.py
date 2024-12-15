import re

# Part 1: Sum of products
def sum_mul_products(corrupted_memory):
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    return sum(int(x) * int(y) for x, y in re.findall(pattern, corrupted_memory))

# Part 2: Process instructions 
def parse_instructions(corrupted_memory):
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)|\b(do|don\'t)\(\)'
    results = []
    for match in re.finditer(pattern, corrupted_memory):
        if match.group(1) and match.group(2):
            results.append((int(match.group(1)), int(match.group(2))))
        elif match.group(3):
            results.append(match.group(3))
    return results


# Read the input file
with open('day3.txt', 'r') as file:
        corrupted_memory = file.read()


# Part 1 Calculation
part1 = sum_mul_products(corrupted_memory)
print(f"Part 1 result is: {part1}")

# Part 2 Calculation
instructions = parse_instructions(corrupted_memory)
do_flag = True
part2 = 0

for i in instructions:
    if isinstance(i, tuple):
        if do_flag:
            part2 += i[0] * i[1]
    elif i == "do":
        do_flag = True
    elif i == "don't":
        do_flag = False

print(f"Part 2 result is: {part2}")
