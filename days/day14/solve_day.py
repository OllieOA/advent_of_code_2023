from collections import Counter
from typing import List

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser


class Day14(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        print(grid)

        for col in range(grid.shape[1]):
            # Find all cases of cube rocks
            blockers = [0] + [x for x in np.where(grid[:, col] == "#")[0].tolist()]

            if len(blockers) == 1:
                # Roll all to the top
                col_breakdown = Counter(grid[:, col])
                new_col = np.array(["O"] * col_breakdown["O"] + ["."] * col_breakdown["."])
                grid[:, col] = new_col
                continue

            new_col = []
            for block_idx in range(len(blockers) - 1):
                print(col, blockers[block_idx], blockers[block_idx + 1])

        print(grid)

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day14(day, use_sample, run_each)
    solver.solve()
