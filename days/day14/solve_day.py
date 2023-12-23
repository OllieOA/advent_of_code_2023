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

    def __tilt_mirror(self, grid: np.array) -> np.array:
        """This function simply rotates the grid in accordance with the rules
        described. We do this by finding the blockers (edge of board or square
        boulder) and then populating the "sub column" with the correct amount.
        Note that this only works to the "north", so when we eventually run
        the full cycle for part 2, we will need to rotate the array.
        """
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

    def __run_cycle(self, grid: np.array) -> np.array:
        """As above, we tilt and rotate. This order is important as the final
        state is NOT a northward tilt in part 2 (as it was for part 1)
        """
        cycling_grid = np.copy(grid)
        for _idx in range(4):
            cycling_grid = self.__tilt_mirror(cycling_grid)
            cycling_grid = np.rot90(cycling_grid, k=3)

        return cycling_grid

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()

        tilted_grid = self.__tilt_mirror(grid)
        total_load = sum([tilted_grid.shape[1] - x for x in np.where(tilted_grid == "O")[0]])

        return total_load

    def part2(self, data: List[str]) -> None:
        """Obviously, we cannot run this 1 billion times. We assume there is a
        pattern and only rotate until we find it. Once we see that a single
        hashed pattern is repeated 3 times, we can safely identify the repeat.

        Then, we identify the offset (everything that has occured once) and can
        apply a modulo to the 1b.
        """
        grid = NumpyArrayParser(data).parse()

        original_grid = np.copy(grid)

        total_full_cycles = 1000000000
        pattern_found = False
        all_grid_configs = []
        while not pattern_found:
            grid = self.__run_cycle(grid)
            boulders = np.where(grid == "O")
            grid_hash_list = [(x, y) for x, y in zip(boulders[0], boulders[1])]
            all_grid_configs.append(tuple(grid_hash_list))
            grid_repeats = Counter(all_grid_configs)
            pattern_found = max(grid_repeats.values()) == 3

        init_offset = len([x for x in grid_repeats.values() if x == 1])
        sequence_len = len([x for x in grid_repeats.values() if x == 2]) + 1

        grid = np.copy(original_grid)
        for idx in range(init_offset + (total_full_cycles - init_offset) % sequence_len):
            grid = self.__run_cycle(grid)

        total_load = sum([grid.shape[1] - x for x in np.where(grid == "O")[0]])
        return total_load


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day14(day, use_sample, run_each)
    solver.solve()
