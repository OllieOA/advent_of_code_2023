from collections import Counter
from itertools import combinations
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NewLineListParser, NumpyArrayParser


OPPOSITES = {".": "#", "#": "."}


class Day13(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __find_reflection(self, grid: np.array, exclude: Tuple[int] = (-1, -1)) -> List[int]:
        """Here, we check if there are two columns next to one another that are
        identical - this is the foundation for a reflection.

        We then step out until we have a fully validated reflection (until the
        edge of the map). We would either exit when a base column or row is
        found, which is our answer (+1 because AoC is doing it one-based).

        We also have an "exclude" field, which is used to specifically exclude
        the original reflection line (expressed as a (row, col) tuple) as we
        specifically want to find alternative maps in part 2.
        """
        for col in range(grid.shape[1] - 1):
            if (col + 1) == exclude[1]:
                continue
            if all([x1 == x2 for x1, x2 in zip(grid[:, col], grid[:, col + 1])]):
                neg_dir = col
                pos_dir = col + 1

                while neg_dir > 0 and pos_dir < (grid.shape[1] - 1):
                    neg_dir -= 1
                    pos_dir += 1
                    if not self.__check_all_same(grid, neg_dir, pos_dir, check_col=True):
                        col = -1
                        break

                if col != -1:
                    return [0, col + 1]

        for row in range(grid.shape[0] - 1):
            if (row + 1) == exclude[0]:
                continue
            if all([y1 == y2 for y1, y2 in zip(grid[row, :], grid[row + 1, :])]):
                neg_dir = row
                pos_dir = row + 1

                while neg_dir > 0 and pos_dir < (grid.shape[0] - 1):
                    neg_dir -= 1
                    pos_dir += 1
                    if not self.__check_all_same(grid, neg_dir, pos_dir, check_col=False):
                        row = -1
                        break

                if row != -1:
                    return [row + 1, 0]

        return [0, 0]

    def __check_all_same(self, grid: np.array, idx1: int, idx2: int, check_col: bool) -> bool:
        """This helper function checks if two arrays are the same, which are
        either a column or a row.
        """
        if check_col:
            return all([x1 == x2 for x1, x2 in zip(grid[:, idx1], grid[:, idx2])])
        return all([x1 == x2 for x1, x2 in zip(grid[idx1, :], grid[idx2, :])])

    def __find_one_off_candidates(self, grid: np.array) -> List[Tuple]:
        """To reduce the search space in part 2, we need to find the rows/cols
        that are one one away from being the same, then it doesn't matter what
        the symbol was; a flip will guarantee the row/col will be the same.

        The trick here is to assert that there is only one False in a similarity
        check.
        """
        candidates = []
        col_pairs = list(combinations(range(grid.shape[1]), r=2))

        for col1, col2 in col_pairs:
            similarities = [x1 == x2 for x1, x2 in zip(grid[:, col1], grid[:, col2])]

            if Counter(similarities)[False] == 1:
                row_idx = similarities.index(False)
                candidates.append((row_idx, col1))

        row_pairs = list(combinations(range(grid.shape[0]), r=2))

        for row1, row2 in row_pairs:
            similarities = [y1 == y2 for y1, y2 in zip(grid[row1, :], grid[row2, :])]

            if Counter(similarities)[False] == 1:
                col_idx = similarities.index(False)
                candidates.append((row1, col_idx))

        return list(set(candidates))

    def part1(self, data: List[str]) -> None:
        """We simply use our __find_reflection function and do the arithmetic as
        instructed.
        """
        mirror_map_lines = NewLineListParser(data).parse()
        mirror_maps = [NumpyArrayParser(x).parse() for x in mirror_map_lines]

        total_rows_cols = [0, 0]

        for mirror_map in mirror_maps:
            total_rows_cols = [
                x1 + x2 for x1, x2 in zip(self.__find_reflection(mirror_map), total_rows_cols)
            ]

        return 100 * total_rows_cols[0] + total_rows_cols[1]

    def part2(self, data: List[str]) -> None:
        """This is a bit more complicated - we are specifically looking for
        alternative maps, so with the candidates for a flip, we make several
        copies of the map with the symbol flipped at the candidate, and then
        search until we find a reflection that gives us a valid row/col (default
        output of __find_reflection is [0, 0]).

        Then, the return arithmetic is the same.
        """
        mirror_map_lines = NewLineListParser(data).parse()
        mirror_maps = [NumpyArrayParser(x).parse() for x in mirror_map_lines]

        total_rows_cols = [0, 0]

        for mirror_map in mirror_maps:
            original_result = tuple(self.__find_reflection(mirror_map))
            candidates_to_test = self.__find_one_off_candidates(mirror_map)

            alt_maps_to_test = []
            for candidate in candidates_to_test:
                new_map = np.copy(mirror_map)
                new_map[candidate] = OPPOSITES[new_map[candidate]]
                alt_maps_to_test.append(new_map)

            for alt_map in alt_maps_to_test:
                res = self.__find_reflection(alt_map, exclude=original_result)
                if any([x != 0 for x in res]):
                    break

            total_rows_cols = [x1 + x2 for x1, x2 in zip(res, total_rows_cols)]

        return 100 * total_rows_cols[0] + total_rows_cols[1]


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day13(day, use_sample, run_each)
    solver.solve()
