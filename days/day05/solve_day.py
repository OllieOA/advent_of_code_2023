import math
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NewLineListParser


class Mapper:
    """The mapper class handles the forward and reverse mapping logic. This
    class will first assume the same value will be returned (default behaviour)
    but then will iterate all the ranges in the Mapper object. The benefit here
    is that range inclusion is a very fast operation as it just compares with
    the range parameters (start, length) rather than generating the entire list
    """

    def __init__(self, components: Tuple[str], range_specs: List[List[int]]) -> None:
        self.src = components[0]
        self.dst = components[1]
        self.range_specs = range_specs

    def get_forward_lookup(self, lookup_val: int) -> int:
        output_val = lookup_val
        for range_spec in self.range_specs:
            if lookup_val in range(range_spec[1], range_spec[1] + range_spec[2]):
                output_val = range_spec[0] + lookup_val - range_spec[1]
        return output_val

    def get_reverse_lookup(self, lookup_val: int) -> int:
        output_val = lookup_val
        for range_spec in self.range_specs:
            if lookup_val in range(range_spec[0], range_spec[0] + range_spec[2]):
                output_val = range_spec[1] + lookup_val - range_spec[0]

        return output_val


class Day05(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.CHAIN = [
            "seed",
            "soil",
            "fertilizer",
            "water",
            "light",
            "temperature",
            "humidity",
            "location",
        ]

    def __build_map_spec(self, data: List[str]) -> None:
        """Here, we simply build the ranges up as specified using the helpful
        Mapper custom class. This class takes the range and generates the
        lookup. The key here is that the mapper only deals with the range
        parameters in the lookup (start, length) rather than the naive approach
        which would have them all generated in a lookup table.
        """
        all_maps = NewLineListParser(data).parse()
        self.seeds = [int(x) for x in all_maps[0][0].split(": ")[-1].split(" ")]

        self.map_specs = {}
        for map_details in all_maps[1:]:
            map_name = map_details[0].replace(" map:", "")

            map_components = (map_name.split("-")[0], map_name.split("-")[-1])

            range_specs = []
            for map_ranges in map_details[1:]:
                range_specs.append([int(x) for x in map_ranges.split(" ")])

            self.map_specs[map_components] = Mapper(map_components, range_specs)

    def __get_lowest_location(self, target_range: List[int]) -> int:
        """This is a pretty naive implementation, which just checks each seed
        and resolves it all the way to the bottom of the chain.

        The only other part to consider is that the "chain" portion here just
        chains together the
        """
        lowest_location = math.inf
        for seed in target_range:
            curr_val = seed
            for idx in range(len(self.CHAIN) - 1):
                lookup = (self.CHAIN[idx], self.CHAIN[idx + 1])
                curr_val = self.map_specs[lookup].get_forward_lookup(curr_val)

            lowest_location = min(lowest_location, curr_val)

        return lowest_location

    def part1(self, data: List[str]) -> None:
        """Explanation is in the helper functions"""
        self.__build_map_spec(data)
        return self.__get_lowest_location(self.seeds)

    def part2(self, data: List[str]) -> None:
        """This was expected, which is why the "reverse lookup" exists in the
        Mapper class, but it is still quite slow at ~2.5 minutes to a solution.

        This works by flipping the problem on its head and checking each
        location in ascending order to find the first time it intersects with
        any ranges in the seeds.

        To optimise this (idea) TODO:
        First, break apart the location ranges and the level of range.
        This becomes the frontier (sorted by lowest level and start of range).
        Keep going like a DFS on the ranges until they are exhausted. When
        a range is identified that has any overlap with the seed ranges,
        select the start range and go from there.
        """
        self.__build_map_spec(data)
        self.seed_ranges = []
        for s_idx in range(0, len(self.seeds), 2):
            self.seed_ranges.append(
                range(self.seeds[s_idx], self.seeds[s_idx] + self.seeds[s_idx + 1])
            )

        curr_location = 0
        solution_found = False
        while True:
            curr_location += 1

            if curr_location % 10000 == 0:
                print(f"Checking {curr_location}...\r", end="\r")

            curr_val = curr_location

            for idx in range(len(self.CHAIN) - 1, 0, -1):
                lookup = (self.CHAIN[idx - 1], self.CHAIN[idx])
                curr_val = self.map_specs[lookup].get_reverse_lookup(curr_val)

            for seed_range in self.seed_ranges:
                solution_found = solution_found or curr_val in seed_range

            if solution_found:
                return curr_location


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day05(day, use_sample, run_each)
    solver.solve()
