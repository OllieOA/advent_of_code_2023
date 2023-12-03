import math
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser

NUMS = "1234567890"


class Day03(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __get_adjacent_positions(self, pos: Tuple[int]) -> List[Tuple]:
        x_pos = [pos[0] - 1, pos[0], pos[0] + 1]
        y_pos = [pos[1] - 1, pos[1], pos[1] + 1]

        all_combos = []
        for x in x_pos:
            for y in y_pos:
                if x < 0 or x >= self.arr.shape[0] or y < 0 or y >= self.arr.shape[1]:
                    continue
                if all([x == pos[0], y == pos[1]]):
                    continue
                all_combos.append((x, y))

        return all_combos

    def __seek_for_number_lr(self, start_pos: Tuple[int]) -> Tuple[List[Tuple[int]], int]:
        tracked_indices = []
        curr_pos = start_pos
        num_str = self.arr[curr_pos[0], curr_pos[1]]

        # Seek left
        curr_pos = (curr_pos[0], curr_pos[1] - 1)
        next_num = self.arr[curr_pos[0], curr_pos[1]]

        while next_num in NUMS:
            num_str = next_num + num_str
            tracked_indices.append(curr_pos)
            curr_pos = (curr_pos[0], curr_pos[1] - 1)
            try:
                next_num = self.arr[curr_pos[0], curr_pos[1]]
            except IndexError:
                break

        # Seek right
        curr_pos = (start_pos[0], start_pos[1] + 1)
        next_num = self.arr[curr_pos[0], curr_pos[1]]

        while next_num in NUMS:
            num_str += next_num
            tracked_indices.append(curr_pos)
            curr_pos = (curr_pos[0], curr_pos[1] + 1)
            try:
                next_num = self.arr[curr_pos[0], curr_pos[1]]
            except IndexError:
                break

        return tracked_indices, int(num_str)

    def part1(self, data: List[str]) -> None:
        self.arr = NumpyArrayParser(data).parse()

        part_nums = []
        considered_positions = set([])
        for i in range(self.arr.shape[0]):
            for j in range(self.arr.shape[1]):
                if self.arr[i, j] in NUMS + ".":
                    continue
                # Now, seek for any valid numbers
                candidate_positions = self.__get_adjacent_positions((i, j))
                for check_pos in candidate_positions:
                    if check_pos in considered_positions:
                        continue
                    if self.arr[check_pos[0], check_pos[1]] not in NUMS:
                        continue

                    single_considered_positions, part_num = self.__seek_for_number_lr(check_pos)
                    considered_positions = considered_positions.union(
                        set(single_considered_positions)
                    )
                    part_nums.append(part_num)

        return sum(part_nums)

    def part2(self, data: List[str]) -> None:
        self.arr = NumpyArrayParser(data).parse()

        gear_ratios = []
        considered_positions = set([])
        for i in range(self.arr.shape[0]):
            for j in range(self.arr.shape[1]):
                if self.arr[i, j] != "*":
                    continue
                gear_parts = []

                # Now, as before seek for any valid numbers. Repeated code but
                # small enough to not get a refactor

                candidate_positions = self.__get_adjacent_positions((i, j))
                for check_pos in candidate_positions:
                    if check_pos in considered_positions:
                        continue
                    if self.arr[check_pos[0], check_pos[1]] not in NUMS:
                        continue

                    single_considered_positions, part_num = self.__seek_for_number_lr(check_pos)
                    considered_positions = considered_positions.union(
                        set(single_considered_positions)
                    )
                    gear_parts.append(part_num)

                if len(gear_parts) == 2:  # Gear identified
                    gear_ratios.append(math.prod(gear_parts))

        return sum(gear_ratios)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day03(day, use_sample, run_each)
    solver.solve()
