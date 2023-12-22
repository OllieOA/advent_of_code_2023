from collections import Counter
import concurrent.futures as cf
from functools import cache
from itertools import product
import os
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
            arrangements.append((arrangement, tuple(spec)))

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

    @cache
    def __dfs(self, sequence: str, spec: Tuple[int]) -> int:
        """Here, we have pretty much directly deployed mgtezak's solution
        https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_12.py
        """
        if not spec:
            return 1 if "#" not in sequence else 0
        spec_len = spec[0]
        if len(sequence) - sum(spec) - len(spec) + 1 < 0:
            return 0  # No more possibilities available

        invalid = any(sequence[x] == "." for x in range(spec_len))
        if len(sequence) == spec_len:
            return 0 if invalid else 1
        valid = not invalid and sequence[spec_len] != "#"

        if sequence[0] == "#":
            return self.__dfs(sequence[spec_len + 1 :].lstrip("."), tuple(spec[1:])) if valid else 0

        skip = self.__dfs(sequence[1:].lstrip("."), spec)
        if not valid:
            return skip
        return skip + self.__dfs(sequence[spec_len + 1 :], tuple(spec[1:]))

    def part2(self, data: List[str]) -> None:
        arrangements = self.__make_arrangements(data, repeats=5)

        total_arrangements = 0

        for arrangement in arrangements:
            sequence, spec = arrangement
            total_arrangements += self.__dfs(sequence, spec)

        return total_arrangements


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day12(day, use_sample, run_each)
    solver.solve()
