from typing import List

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions, get_manhattan_dist

# CORRECT ANSWER IS 3642

X = 1


class Day21(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        reachable_in_x_tiles = {}
        start_node = tuple([int(x) for x in np.where(grid == "S")])

        # Break into 8s
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if get_manhattan_dist((i, j), start_node) > 64:
                    continue  # Not reachable in this test

                curr_start_node = (i, j)
                steps = {0: [curr_start_node]}
                for idx in range(X):
                    next_steps = []
                    for start_point in steps[idx]:
                        adjacent_positions = get_adjacent_positions(
                            start_point, grid.shape, include_diagonals=False
                        )
                        for adjacent_position in adjacent_positions:
                            if grid[adjacent_position] != "#":
                                next_steps.append(adjacent_position)
                    steps[idx + 1] = list(set(next_steps))

                reachable_in_x_tiles[curr_start_node] = steps[X]

        outer_steps = {0: [start_node]}
        for idx in range(64 // X):
            next_steps = []
            for step in outer_steps[idx]:
                next_steps.extend(reachable_in_x_tiles[step])

            outer_steps[idx + 1] = list(set(next_steps))

        return len(outer_steps[idx + 1])

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day21(day, use_sample, run_each)
    solver.solve()
