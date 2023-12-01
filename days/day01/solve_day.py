import re
from typing import List

from solver import Solver

LETTERS_TO_NUMS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


class Day01(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        """Simply only take what is a digit, and then combine the first and
        last one (this will still work if there is only one)

        """
        calibrations = []
        for line in data:
            new_calib = [x for x in line if x.isdigit()]
            calibrations.append(int(new_calib[0] + new_calib[-1]))

        return sum(calibrations)

    def part2(self, data: List[str]) -> None:
        """Here we do a similar thing, though we also track the occurences of
        any individual word. The trick is that overlapping words MUST COUNT
        separately (something I did not grasp for stupidly long), and then we
        only need to replace the index of occurence with the digit for the
        concatenation algorithm to work.
        """
        calibrations = []
        for line in data:
            nums_in_str = {}
            for num_str in LETTERS_TO_NUMS.keys():
                str_locations = [m.start() for m in re.finditer(num_str, line)]
                for str_location in str_locations:
                    nums_in_str[str_location] = num_str

            for idx, num_str in nums_in_str.items():
                line = line[:idx] + LETTERS_TO_NUMS[num_str] + line[idx + 1 :]

            new_calib = [x for x in line if x.isdigit()]
            calibrations.append(int(new_calib[0] + new_calib[-1]))

        return sum(calibrations)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day01(day, use_sample, run_each)
    solver.solve()
