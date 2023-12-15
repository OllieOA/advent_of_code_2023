from typing import List

from solver import Solver


class Day15(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        cases = data[0].split(",")

        case_history = []
        for case in cases:
            curr_num = 0
            for c in case:
                curr_num += ord(c)
                curr_num *= 17
                curr_num %= 256
            case_history.append(curr_num)

        return sum(case_history)

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day15(day, use_sample, run_each)
    solver.solve()
