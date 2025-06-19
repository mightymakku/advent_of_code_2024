l1 = []
l2 = []

with open(r'day01_2_input.txt') as f:
    lines = f.readlines()
    for line in lines:
        x, y = line.split('   ')
        l1.append(int(x))
        l2.append(int(y))

similarity_score = sum([i * l2.count(i) for i in l1])

print(f'{similarity_score=}')
