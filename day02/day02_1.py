from typing import Sequence


class Report:
    def __init__(self, events: Sequence[int]):
        self._events = list(events)

    def is_valid(self) -> bool:
        if sorted(self._events) != self._events and sorted(self._events, reverse=True) != self._events:
            return False

        for i in range(0, len(self._events) - 1):
            diff = abs(self._events[i] - self._events[i + 1])
            if diff < 1 or diff > 3:
                return False

        return True


def read_reports(path: str) -> Sequence[Report]:
    with open(path, mode='r') as f:
        lines = f.readlines()
        return [Report([int(i) for i in line.split(' ')]) for line in lines]


reports = read_reports('day02_1_input.txt')
valid_count = len([r for r in reports if r.is_valid()])

print(f'{valid_count=}')
