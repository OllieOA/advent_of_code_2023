from typing import List

from solver import Solver
from utils.parsers import NewLineListParser, NumpyArrayParser


class Day13(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        mirror_map_lines = NewLineListParser(data).parse()
        mirror_maps = [NumpyArrayParser(x).parse() for x in mirror_map_lines]

        total_rows = 0
        total_cols = 0

        for mirror_map in mirror_maps:
            for col in range(mirror_map.shape[1] - 1):
                if all([x1 == x2 for x1, x2 in zip(mirror_map[:, col], mirror_map[:, col + 1])]):
                    neg_dir = col
                    pos_dir = col + 1

                    while neg_dir > 0 and pos_dir < (mirror_map.shape[1] - 1):
                        neg_dir -= 1
                        pos_dir += 1
                        if not all(
                            [
                                x1 == x2
                                for x1, x2 in zip(mirror_map[:, neg_dir], mirror_map[:, pos_dir])
                            ]
                        ):
                            col = 0
                            break

                    total_cols += col + 1

            for row in range(mirror_map.shape[0] - 1):
                if all([y1 == y2 for y1, y2 in zip(mirror_map[row, :], mirror_map[row + 1, :])]):
                    neg_dir = row
                    pos_dir = row + 1

                    while neg_dir > 0 and pos_dir < (mirror_map.shape[0] - 1):
                        neg_dir -= 1
                        pos_dir += 1
                        if not all(
                            [
                                y1 == y2
                                for y1, y2 in zip(mirror_map[neg_dir, :], mirror_map[pos_dir, :])
                            ]
                        ):
                            row = 0
                            break

                    total_rows += row + 1

        return total_cols + 100 * total_rows

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day13(day, use_sample, run_each)
    solver.solve()
