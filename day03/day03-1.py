import re


def mul(x: int, y: int) -> int:
    return x * y


with open(r'day03-1_input.txt') as f:
    input = f.read()

matches = re.findall('mul\\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\\)', input)

total = sum([eval(m) for m in matches])
print(f'{total=}')
