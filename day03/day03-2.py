import re


def mul(x: int, y: int) -> int:
    return x * y


with open(r'day03-2_input.txt') as f:
    input = f.read()

matches = re.findall('mul\\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\\)|don\'t\\(\\)|do\\(\\)', input)

total = 0
do_mul = True

for m in matches:
    if m == 'do()':
        do_mul = True
    elif m == 'don\'t()':
        do_mul = False
    else:
        if do_mul:
            total += eval(m)

print(f'{total=}')
