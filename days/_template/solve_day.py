from typing import List

from solver import Solver


class DayX(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        pass

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = DayX(day, use_sample, run_each)
    solver.solve()
