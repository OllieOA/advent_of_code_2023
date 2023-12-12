from collections import Counter
from itertools import product
from typing import List, Tuple

from solver import Solver


class Day12(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day
        self.OPTS = [".", "#"]

    def __make_arrangements(self, data: List[str], repeats: int = 1) -> List[Tuple]:
        arrangements = []
        for line in data:
            arrangement, spec = line.split(" ")

            arrangement = "?".join([arrangement] * repeats)
            spec = [int(x) for x in spec.split(",")] * repeats
            arrangements.append((arrangement, spec))

        return arrangements

    def __check_valid(self, arrangement: List[str], spec: List[int]) -> bool:
        continuous_ranges = [len(x) for x in arrangement.split(".") if len(x) > 0]
        if len(continuous_ranges) != len(spec):
            return False

        return all([i == j for i, j in zip(continuous_ranges, spec)])

    def __check_total_arrangements(self, arrangement: List[str], spec: List[int]) -> int:
        point_opts = [[x] if x != "?" else self.OPTS for x in arrangement]
        possibilities = product(*point_opts)
        filtered_possibilities = ["".join(x) for x in possibilities if Counter(x)["#"] == sum(spec)]
        num_arrangements = 0
        for possibility in filtered_possibilities:
            if self.__check_valid(possibility, spec):
                num_arrangements += 1

        return num_arrangements

    def part1(self, data: List[str]) -> None:
        arrangements = self.__make_arrangements(data, repeats=1)

        total_arrangements = 0
        for arrangement, spec in arrangements:
            total_arrangements += self.__check_total_arrangements(arrangement, spec)

        return total_arrangements

    def part2(self, data: List[str]) -> None:
        arrangements = self.__make_arrangements(data, repeats=5)
        total_arrangements = 0
        for arrangement, spec in arrangements:
            total_arrangements += self.__check_total_arrangements(arrangement, spec)

        return total_arrangements


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day12(day, use_sample, run_each)
    solver.solve()
