try:
    with open("day1.txt", "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("File not found")
    exit()

left_list = []
right_list = []

for line in lines:
    try:
        left, right = map(int, line.strip().split())
        left_list.append(left)
        right_list.append(right)
    except ValueError:
        print("Invalid input format in file")
        exit()

left_list.sort()
right_list.sort()

# Part 1: Total distance
total_distance = 0
for i in range(len(left_list)):
    total_distance += abs(left_list[i] - right_list[i])

# Part 2: Similarity score
similarity_score = 0
for left_val in left_list:
    similarity_score += left_val * right_list.count(left_val)

print(f"Part 1: {total_distance}")
print(f"Part 2: {similarity_score}")