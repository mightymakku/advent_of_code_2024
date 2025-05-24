from typing import Sequence


class Report:
    def __init__(self, events: Sequence[int]):
        self._events = list(events)

    @staticmethod
    def _diffs_valid(events: Sequence[int]) -> bool:
        for i in range(0, len(events) - 1):
            diff = abs(events[i] - events[i + 1])
            if diff < 1 or diff > 3:
                return False
        return True

    def is_valid(self) -> bool:
        for x in range(0, len(self._events)):
            dampened = self._events.copy()
            dampened.pop(x)

            if sorted(dampened) != dampened and sorted(dampened, reverse=True) != dampened:
                continue

            if not Report._diffs_valid(dampened):
                continue

            return True

        return False


def read_reports(path: str) -> Sequence[Report]:
    with open(path, mode='r') as f:
        lines = f.readlines()
        return [Report([int(i) for i in line.split(' ')]) for line in lines]


reports = read_reports('day02-2_input.txt')
valid_count = len([r for r in reports if r.is_valid()])

print(f'{valid_count=}')
