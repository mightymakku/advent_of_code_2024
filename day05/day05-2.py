from dataclasses import dataclass


@dataclass
class Rule:
    first: int
    second: int

    def validate_update(self, update: list[int]) -> bool:
        if self.first in update and self.second in update:
            return update.index(self.first) < update.index(self.second)
        return True

    def fix_update(self, update: list[int]) -> None:
        if self.validate_update(update):
            return
        update.remove(self.first)
        update.insert(update.index(self.second), self.first)


def read_input(filename):
    rules: list[Rule] = []
    updates: list[list[int]] = []

    with open(filename, 'r') as f:
        for line in f:
            if '|' in line:
                first, second = line.split('|')
                rules.append(Rule(first=int(first), second=int(second)))
            elif ',' in line:
                pages = (int(p) for p in line.strip().split(','))
                updates.append(list(pages))

    return (rules, updates)


if __name__ == '__main__':
    import sys
    input_filename = sys.argv[1]
    rules, updates = read_input(input_filename)
    fixed_updates = []

    for update in updates:
        if not all((r.validate_update(update) for r in rules)):
            while any((not r.validate_update(update) for r in rules)):
                for rule in rules:
                    rule.fix_update(update)
            fixed_updates.append(update)

    middle_pagenumbers_sum = sum((u[int(len(u)/2)] for u in fixed_updates))
    print(f'{middle_pagenumbers_sum=}')
