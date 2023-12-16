from typing import List

from solver import Solver


class Day15(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __get_hash(self, case: str) -> int:
        curr_num = 0
        for c in case:
            curr_num += ord(c)
            curr_num *= 17
            curr_num %= 256

        return curr_num

    def part1(self, data: List[str]) -> None:
        cases = data[0].split(",")
        case_history = [self.__get_hash(case) for case in cases]

        return sum(case_history)

    def part2(self, data: List[str]) -> None:
        cases = data[0].split(",")

        boxes = {}

        for case in cases:
            case_breakdown = case.split("=")
            label = case_breakdown[0]

            target_box = self.__get_hash(label.replace("-", ""))
            if target_box not in boxes:
                boxes[target_box] = {}

            if label.endswith("-"):
                if label[:-1] in boxes[target_box]:
                    del boxes[target_box][label[:-1]]
            else:
                boxes[target_box][label] = int(case_breakdown[-1])

        focus_power = 0
        for box, box_breakdown in boxes.items():
            for slot, focal in enumerate(box_breakdown.values()):
                focus_power += (box + 1) * (slot + 1) * focal

        return focus_power


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day15(day, use_sample, run_each)
    solver.solve()
