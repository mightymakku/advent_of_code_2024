import sys


class XmasFinder:
    @property
    def count(self):
        return self._total_count

    @staticmethod
    def _check_word(word):
        return word == 'MAS' or word[::-1] == 'MAS'

    def _check_topleft_to_bottom_right(self):
        tl = self._input[self._current_y - 1][self._current_x - 1]
        md = self._input[self._current_y][self._current_x]
        br = self._input[self._current_y + 1][self._current_x + 1]

        word = ''.join([tl, md, br])
        return XmasFinder._check_word(word)

    def _check_bottomleft_to_topright(self):
        bl = self._input[self._current_y + 1][self._current_x - 1]
        md = self._input[self._current_y][self._current_x]
        tr = self._input[self._current_y - 1][self._current_x + 1]

        word = ''.join([bl, md, tr])
        return XmasFinder._check_word(word)

    def _check_x_mas_hit_on_current_position(self):
        if self._input[self._current_y][self._current_x] != 'A':
            return False
        return self._check_topleft_to_bottom_right() and self._check_bottomleft_to_topright()

    def __call__(self, input):
        self._input = input
        self._max_y = len(self._input)
        self._max_x = len(self._input[0])
        self._total_count = 0

        for y in range(1, self._max_y - 1):
            for x in range(1, self._max_x - 1):
                self._current_x = x
                self._current_y = y
                if self._check_x_mas_hit_on_current_position():
                    self._total_count += 1

        return self._total_count


if __name__ == '__main__':
    input_filename = sys.argv[1]

    input = []

    with open(input_filename, 'r') as input_file:
        for line in input_file:
            input.append(line.strip())

    finder = XmasFinder()
    finder(input)
    print(f'{finder.count=}')
