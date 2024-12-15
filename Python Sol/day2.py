def is_safe_report(r):
    if len(r)<2:return True
    diff=r[1]-r[0]
    if diff==0:return False
    dec=diff<0
    for i in range(1,len(r)):
        d=r[i]-r[i-1]
        if d==0 or abs(d)>3 or (dec and d>=0) or (not dec and d<=0):return False
    return True

def is_safe_with_one_removal(r):
    return is_safe_report(r) or any(is_safe_report(r[:i]+r[i+1:]) for i in range(len(r)))

reports=[list(map(int,line.split()))for line in open('day2.txt')]

# Part 1:
print(sum(is_safe_report(r)for r in reports))

# Part 2:
print(sum(is_safe_with_one_removal(r)for r in reports))
