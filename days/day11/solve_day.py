from itertools import combinations
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser


class Day11(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __get_manhattan_distance(
        self,
        point1: Tuple[int],
        point2: Tuple[int],
        num_horiz_offsets: int = 0,
        num_vert_offsets: int = 0,
        offset_multiplier: int = 0,
    ) -> int:
        """Here, the trick is that we need to consider the amount of extra lines
        introduced between each galaxy, which we do with the offset number and
        multiplier. Also note the "offset_multipler - 1" as we need to remember
        that the original empty row is already included in the count.

        Otherwise, this is a simple Manhattan distance of height + width to
        calculate the number of steps.
        """

        horiz_dist = abs(point1[0] - point2[0]) + (num_horiz_offsets * (offset_multiplier - 1))
        vert_dist = abs(point1[1] - point2[1]) + (num_vert_offsets * (offset_multiplier - 1))

        return horiz_dist + vert_dist

    def __find_expansions(self, grid: np.array) -> Tuple[List[int]]:
        """The check here is to find rows/cols where the number of unique types
        is of len(1). While it should already be safe, we also assert that the
        first element is the empty element in case there is a full row/col of
        cells that are galaxies."""

        expand_cols = []
        expand_rows = []
        for col in range(grid.shape[1]):
            if len(np.unique(grid[:, col])) == 1 and grid[0, col] == ".":
                expand_cols.append(col)
        for row in range(grid.shape[0]):
            if len(np.unique(grid[row, :])) == 1 and grid[row, 0] == ".":
                expand_rows.append(row)

        return expand_cols, expand_rows

    def __find_galaxy(self, grid: np.array) -> List[Tuple[int]]:
        """Nothing tricky here - just find the galaxies in the array"""
        galaxy_locations = []

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == "#":
                    galaxy_locations.append((i, j))
        return galaxy_locations

    def __get_offsets(
        self, point1: Tuple[int], point2: Tuple[int], expand_cols: List[int], expand_rows: List[int]
    ) -> Tuple[int]:
        """Here we need to count the number of offsets between two points after
        they have been identified in . This
        """
        horiz_offsets = 0
        for col in expand_cols:
            if min(point1[1], point2[1]) <= col <= max(point1[1], point2[1]):
                horiz_offsets += 1

        vert_offsets = 0
        for row in expand_rows:
            if min(point1[0], point2[0]) <= row <= max(point1[0], point2[0]):
                vert_offsets += 1

        return horiz_offsets, vert_offsets

    def __get_galaxy_lens(self, grid: np.array, offset_multiplier: int) -> int:
        """We combine what we have found above to pass in the pair of points and
        the number of horizontal/vertical offsets required for each point.
        """
        expand_cols, expand_rows = self.__find_expansions(grid)

        galaxy_locations = self.__find_galaxy(grid)

        galaxy_pairs = list(combinations(galaxy_locations, r=2))
        galaxy_offsets = [
            self.__get_offsets(x, y, expand_cols, expand_rows) for x, y in galaxy_pairs
        ]

        galaxy_lens = []
        for galaxy_pair, galaxy_offsets in zip(galaxy_pairs, galaxy_offsets):
            x, y = galaxy_pair
            horiz_offset, vert_offset = galaxy_offsets
            galaxy_lens.append(
                self.__get_manhattan_distance(x, y, horiz_offset, vert_offset, offset_multiplier)
            )

        return sum(galaxy_lens)

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        offset_multiplier = 2

        return self.__get_galaxy_lens(grid, offset_multiplier)

    def part2(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        offset_multiplier = 1000000
        return self.__get_galaxy_lens(grid, offset_multiplier)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day11(day, use_sample, run_each)
    solver.solve()
