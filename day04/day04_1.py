import sys


class XmasFinder:
    def __init__(self, input):
        self._input = input

    @property
    def count(self):
        return self._total_count

    def _get_xmas_hits_of_current_position(self):
        if self._input[self._current_y][self._current_x] != 'X':
            return 0

        hits = 0
        for check in (
                self._check_forward,
                self._check_backward,
                self._check_downward,
                self._check_upward,
                self._check_north_east,
                self._check_north_west,
                self._check_south_east,
                self._check_south_west,
        ):
            if check():
                hits += 1

        return hits

    @staticmethod
    def _check_word(word):
        return word == 'XMAS'

    def _check_forward(self):
        word = self._input[self._current_y][self._current_x:self._current_x + 4]
        return XmasFinder._check_word(word)

    def _check_backward(self):
        word = self._input[self._current_y][self._current_x - 3:self._current_x + 1]
        return XmasFinder._check_word(word[::-1])

    def _check_downward(self):
        lines = self._input[self._current_y:self._current_y + 4]
        word = ''.join([line[self._current_x] for line in lines])
        return XmasFinder._check_word(word)

    def _check_upward(self):
        lines = self._input[self._current_y - 3:self._current_y + 1]
        word = ''.join([line[self._current_x] for line in lines])
        return XmasFinder._check_word(word[::-1])

    def _check_north_east(self):
        if self._current_x + 4 > self._max_x:
            return False

        lines = self._input[self._current_y - 3:self._current_y + 1]

        if len(lines) < 4:
            return False

        parts = []

        for i, line in enumerate(lines):
            x = 3 - i
            parts.append(line[self._current_x + x])

        word = ''.join(parts)
        return XmasFinder._check_word(word[::-1])

    def _check_north_west(self):
        if self._current_x - 3 < 0:
            return False

        lines = self._input[self._current_y - 3:self._current_y + 1]

        if len(lines) < 4:
            return False

        parts = []

        for i, line in enumerate(lines):
            x = i - 3
            parts.append(line[self._current_x + x])

        word = ''.join(parts)
        return XmasFinder._check_word(word[::-1])

    def _check_south_east(self):
        if self._current_x + 4 > self._max_x:
            return False

        lines = self._input[self._current_y:self._current_y + 4]

        if len(lines) < 4:
            return False

        parts = []

        for i, line in enumerate(lines):
            parts.append(line[self._current_x + i])

        word = ''.join(parts)
        return XmasFinder._check_word(word)

    def _check_south_west(self):
        if self._current_x - 3 < 0:
            return False

        lines = self._input[self._current_y:self._current_y + 4]

        if len(lines) < 4:
            return False

        parts = []

        for i, line in enumerate(lines):
            parts.append(line[self._current_x - i])

        word = ''.join(parts)
        return XmasFinder._check_word(word)


    def __call__(self):
        self._max_x = len(self._input[0])
        self._max_y = len(self._input)
        self._total_count = 0
        for y in range(self._max_y):
            for x in range(self._max_x):
                self._current_x = x
                self._current_y = y
                self._total_count += self._get_xmas_hits_of_current_position()


if __name__ == '__main__':
    input_filename = sys.argv[1]

    input = []

    with open(input_filename, 'r') as input_file:
        for line in input_file:
            input.append(line.strip())

    finder = XmasFinder(input)
    finder()
    print(f'{finder.count=}')
