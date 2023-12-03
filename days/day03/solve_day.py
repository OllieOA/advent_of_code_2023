import math
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
import utils.grid_utils as grid_utils

NUMS = "1234567890"


class Day03(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __seek_for_number_lr(self, start_pos: Tuple[int]) -> Tuple[List[Tuple[int]], int]:
        """Here, we start from a position and then seek left and right for
        digits (until hitting anything not in NUMS). This could be compressed
        into a single while loop definition in a for loop over directions
        [-1, 1], but cbf.
        """
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
        """We seek for any symbol character (note, we are using the negative
        here, and finding anything not in the digits or the period `.` as we
        do not know the full list of symbols used).

        From this point, we consider each candidate adjacent position, and then
        check if there is a digit present. If so, we extract it using the above
        function, and importantly, we track what positions we have visited.
        This is important because we use this to not double up any extractions.
        """
        self.arr = NumpyArrayParser(data).parse()

        part_nums = []
        considered_positions = set([])
        for i in range(self.arr.shape[0]):
            for j in range(self.arr.shape[1]):
                if self.arr[i, j] in NUMS + ".":
                    continue
                # Now, seek for any valid numbers
                candidate_positions = grid_utils.get_adjacent_positions((i, j), self.arr.shape)
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
        """Very similar to the above, though we only need to act when the
        symbol is a *. If there are exactly two numbers found using the same
        logic as in part 1, then we consider it a valid gear ratio and add it
        to the list.
        """
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

                candidate_positions = grid_utils.get_adjacent_positions((i, j), self.arr.shape)
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
