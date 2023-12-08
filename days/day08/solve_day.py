from copy import deepcopy
import math
from typing import List

from solver import Solver


class Day08(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __make_grid(self, data: List[str]) -> None:
        """Simply build the grid to be easily indexed"""
        instructions = [x for x in data[0]]
        grid_info = {}

        for line in data[2:]:
            line = line.replace(" ", "")
            node, lr_map = line.split("=", maxsplit=2)
            l, r = lr_map.replace("(", "").replace(")", "").split(",", maxsplit=2)
            grid_info[node] = {"L": l, "R": r}

        self.instructions = instructions
        self.grid_info = grid_info

    def part1(self, data: List[str]) -> None:
        """This just simulates the process until the node is
        encountered. Nothing particularly clever here.
        """
        self.__make_grid(data)
        curr_node = "AAA"

        instructions = deepcopy(self.instructions)

        steps = 0
        while curr_node != "ZZZ":
            curr_instruction = instructions.pop(0)
            instructions += [curr_instruction]
            curr_node = self.grid_info[curr_node][curr_instruction]
            steps += 1

        return steps

    def part2(self, data: List[str]) -> None:
        """Here, we use the trick of the lowest common multiple (spoiled
        for me in the subreddit). As long as we efficiently understand
        the length of each "loop" to the end node, we can just find the
        LCM and that must be the solution.
        """
        self.__make_grid(data)
        curr_nodes = [x for x in self.grid_info.keys() if x.endswith("A")]
        instructions = deepcopy(self.instructions)

        totals_steps = []
        for curr_node in curr_nodes:
            steps = 0
            while not curr_node.endswith("Z"):
                curr_instruction = instructions.pop(0)
                instructions += [curr_instruction]
                curr_node = self.grid_info[curr_node][curr_instruction]
                steps += 1
            instructions = deepcopy(self.instructions)
            totals_steps.append(steps)

        return math.lcm(*totals_steps)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day08(day, use_sample, run_each)
    solver.solve()
