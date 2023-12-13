from collections import Counter
import concurrent.futures as cf
from functools import cache
from itertools import product
import os
from typing import List, Tuple

from tqdm import tqdm

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

    @cache
    def __check_partially_valid(self, arrangement: str, spec: Tuple[int], full_len: int) -> bool:
        arrangement_breakdown = Counter(arrangement)
        sum_spec = sum(spec)
        if arrangement_breakdown.get("#", 0) > sum_spec:
            # print(f"{arrangement}: RETURNING 1")
            return False
        if (
            arrangement_breakdown.get(".", 0) > (full_len - sum_spec)
            and "#" not in arrangement_breakdown.keys()
        ):
            # print(f"{arrangement}: RETURNING 2")
            return False

        continuous_ranges = [len(x) for x in arrangement.split(".") if len(x) > 0]

        if any([x > y for x, y in zip(continuous_ranges, spec)]):
            # print(f"{arrangement}: RETURNING 3")
            # for x, y in zip(continuous_ranges, spec):
            #     print(f"{x} > {y}")
            return False

        return True

    def __process_single_arrangement(self, line: str, repeats: int) -> int:
        arrangement, spec = line.split(" ")
        arrangement = "?".join([arrangement] * repeats)
        spec = tuple([int(x) for x in spec.split(",")] * repeats)

        valid_arrangements = [""]
        curr_idx = -1
        arrangement_len = len(arrangement)
        for _idx in tqdm(range(arrangement_len)):
            next_arrangements = []
            curr_idx += 1
            next_char = arrangement[curr_idx]
            if next_char != "?":
                next_arrangements = [x + next_char for x in valid_arrangements]
            else:
                next_arrangements = [x + "." for x in valid_arrangements] + [
                    x + "#" for x in valid_arrangements
                ]

            # print(f"BEFORE FILTER: {next_arrangements}")
            # Check the logic of each arrangement
            valid_arrangements = [
                x
                for x in next_arrangements
                if self.__check_partially_valid(x, spec, arrangement_len)
            ]
            # print(f"AFTER FILTER: {valid_arrangements}")
            # print("----")
            # if curr_idx > 10:
            #     raise

        return len([x for x in valid_arrangements if self.__check_valid(x, spec)])

    def __make_all_valid_arrangements(self, data: List[str], repeats: int = 1) -> int:
        all_valid_arrangements = 0
        with cf.ThreadPoolExecutor(max_workers=2) as pool:
            executions = []
            for line in data:
                executions.append(pool.submit(self.__process_single_arrangement, line, repeats))

            for execution in tqdm(executions):
                all_valid_arrangements += execution.result()

        return all_valid_arrangements

    def part2(self, data: List[str]) -> None:
        return self.__make_all_valid_arrangements(data, repeats=5)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day12(day, use_sample, run_each)
    solver.solve()
