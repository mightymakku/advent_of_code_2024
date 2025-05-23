l1 = []
l2 = []

with open(r'day01-1_input.txt') as f:
    lines = f.readlines()
    for line in lines:
        x, y = line.split('   ')
        l1.append(int(x))
        l2.append(int(y))

l1.sort()
l2.sort()

total_distance = sum([abs(l1[i] - l2[i]) for i in range(0, len(l1))])

print(f'{total_distance=}')
