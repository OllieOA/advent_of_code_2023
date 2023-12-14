from collections import Counter
from typing import List, Dict

import numpy as np
from tqdm import tqdm

from solver import Solver
from utils.parsers import NumpyArrayParser


class Day14(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __tilt_mirror(self, grid: np.array, pre_check: Dict = {}) -> np.array:
        grid_str = str(grid)
        if grid_str in pre_check:
            return pre_check[grid_str]

        mutate_grid = np.copy(grid)

        for col in range(mutate_grid.shape[1]):
            blockers = [0] + [x for x in np.where(mutate_grid[:, col] == "#")[0].tolist()]

            new_col = []
            for block_idx in range(len(blockers)):
                if block_idx == (len(blockers) - 1):
                    col_range = mutate_grid[blockers[block_idx] :, col]
                else:
                    col_range = mutate_grid[blockers[block_idx] : blockers[block_idx + 1], col]

                col_breakdown = Counter(col_range)
                new_col.extend(["O"] * col_breakdown["O"] + ["."] * col_breakdown["."])
                if block_idx < (len(blockers) - 1):
                    new_col.append("#")
            mutate_grid[:, col] = np.array(new_col)

        pre_check[grid_str] = mutate_grid

        return mutate_grid

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()

        tilted_grid = self.__tilt_mirror(grid)
        total_load = sum([tilted_grid.shape[1] - x for x in np.where(tilted_grid == "O")[0]])

        return total_load

    def part2(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()

        cache = {}
        for _idx in tqdm(range(1000000000)):
            new_grid = self.__tilt_mirror(grid, cache)
            grid = np.rot90(new_grid)
            print(f"CACHE_SIZE {len(cache)}")

        total_load = sum([new_grid.shape[1] - x for x in np.where(new_grid == "O")[0]])

        return total_load


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day14(day, use_sample, run_each)
    solver.solve()
