from typing import Generator
from enum import Enum
from dataclasses import dataclass


class EquationOperator(Enum):
    Add: str = '+'
    Multiply: str = '*'


@dataclass
class CalibrationEquation:
    testvalue: int
    numbers: list[int]

    @classmethod
    def from_inputline(cls, line: str) -> 'CalibrationEquation':
        testvalue_str, numbers_str = line.strip().split(': ')
        testvalue = int(testvalue_str)
        numbers = [int(n) for n in numbers_str.split(' ')]
        return cls(testvalue=testvalue, numbers=numbers)

    def __str__(self) -> str:
        return f'{self.testvalue}: {" ".join((str(n) for n in self.numbers))}'

    def _get_operator_permutations_list(self) -> list[list[EquationOperator]]:
        operators = [eo for eo in EquationOperator]
        operators_count = len(operators)
        operator_gaps_count = len(self.numbers) - 1
        rowcount = pow(operators_count, operator_gaps_count)
        operator_permutations_list = []
        for i in range(rowcount):
            operator_permutations_list.append([])
            for j in range(operator_gaps_count):
                operator_index = (i // int(rowcount / pow(2, (j + 1)))) % operators_count
                operator_permutations_list[i].append(operators[operator_index])
        return operator_permutations_list

    def is_solvable(self) -> bool:
        operator_permuations_list = self._get_operator_permutations_list()
        for operator_permutations in operator_permuations_list:
            equation_str = ''
            for i in range(len(self.numbers)):
                equation_str += str(self.numbers[i])
                if i > 0:
                    equation_str += ')'
                if i < len(operator_permutations):
                    equation_str = f'({equation_str}{operator_permutations[i].value}'
            result = int(eval(equation_str))
            if result == self.testvalue:
                return True
        return False


def parse_input(input_filename: str) -> Generator[CalibrationEquation]:
    with open(input_filename, 'r') as f:
        for line in f:
            yield CalibrationEquation.from_inputline(line)


if __name__ == '__main__':
    import sys
    input_filename = sys.argv[1]
    calibration_equations = parse_input(input_filename)
    solvable_testvalues_sum = sum(ce.testvalue for ce in calibration_equations if ce.is_solvable())
    print(f'{solvable_testvalues_sum}')
