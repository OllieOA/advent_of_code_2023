from collections import Counter
from typing import List, Dict

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser


class Day14(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __tilt_mirror_with_cache(self, grid: np.array, cache: Dict) -> np.array:
        grid_str = str(grid)
        if grid_str in cache:
            return cache[grid_str]

        new_grid = self.__tilt_mirror(grid)
        cache[grid_str] = new_grid
        return new_grid

    def __tilt_mirror(self, grid: np.array) -> np.array:
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

        return mutate_grid

    def __run_cycle(self)

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()

        tilted_grid = self.__tilt_mirror(grid)
        total_load = sum([tilted_grid.shape[1] - x for x in np.where(tilted_grid == "O")[0]])

        return total_load

    def part2(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()

        original_grid = np.copy(grid)

        total_full_cycles = 1000000000
        pattern_found = False
        all_grid_configs = []
        turns = 0
        while not pattern_found:
            new_grid = self.__tilt_mirror(grid)
            if turns % 4 == 3:
                north_aligned_grid_str = str(np.rot90(new_grid, k=turns)) + str((turns % 4))
                # print(f"\ncycle {turns//4+1}\n{north_aligned_grid_str}\n")
                all_grid_configs.append(north_aligned_grid_str)
                grid_repeats = Counter(all_grid_configs)
                pattern_found = max(grid_repeats.values()) == 5
            grid = np.rot90(new_grid, k=3)
            turns += 1

        # raise
        init_offset = len([x for x in grid_repeats.values() if x == 1])
        sequence_len = len([x for x in grid_repeats.values() if x == 4]) + 1

        cycles_required = total_full_cycles % sequence_len + init_offset
        print(
            f"{cycles_required} modifications required - {init_offset} init offset, {sequence_len} seq len"
        )

        turns = 0
        cycles = 0
        grid = np.copy(original_grid)
        cache = {}
        # while cycles < cycles_required:
        for c in range(cycles_required):
            while turns < 4:
                new_grid = self.__tilt_mirror_with_cache(grid, cache)
                if turns % 4 == 3:
                    cycles += 1
                    # print(f"POST CYCLE {cycles} GRID\n{np.rot90(new_grid, k=turns)}\n")
                grid = np.rot90(new_grid, k=3)
                turns += 1
            # print(np.rot90(new_grid, k=turns - 1))
            turns = 0

        new_grid = np.rot90(new_grid, k=turns - 1)
        print(f"FINAL STATE\n{new_grid}")

        total_load = sum([new_grid.shape[1] - x for x in np.where(new_grid == "O")[0]])
        # print(f"{i}: {total_load}")

        return total_load


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day14(day, use_sample, run_each)
    solver.solve()
