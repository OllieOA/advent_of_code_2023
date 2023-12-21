from typing import List, Tuple, Dict

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions, get_manhattan_dist

# CORRECT ANSWER IS 3642

X_P1 = 64
X_P2 = 100


class Day21(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __get_adjacent_positions_and_maps(
        self, pos_map: Tuple[Tuple[int]], arr_shape: Tuple[int]
    ) -> List[Tuple[Tuple[int]]]:
        pos, map_coord = pos_map
        base_positions = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ]

        new_positions = []
        for pos in base_positions:
            x, y = pos
            map_modifier = (0, 0)
            if x < 0:
                map_modifier = (-1, 0)
                pos = (arr_shape[0] - 1, y)
            elif x >= arr_shape[0]:
                map_modifier = (1, 0)
                pos = (0, y)
            elif y < 0:
                map_modifier = (0, -1)
                pos = (x, arr_shape[1] - 1)
            elif y >= arr_shape[1]:
                map_modifier = (0, 1)
                pos = (x, 0)

            modified_map_coord = (m1 + m2 for m1, m2 in zip(map_coord, map_modifier))
            new_positions.append((pos, modified_map_coord))

        return new_positions

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        start_node = tuple([int(x) for x in np.where(grid == "S")])
        adjacent_garden_tile_lookup = {}

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if get_manhattan_dist((i, j), start_node) > X_P1:
                    continue  # Not reachable in this test

                curr_start_node = (i, j)
                adjacent_garden_tile_lookup[curr_start_node] = []
                adjacent_positions = get_adjacent_positions(
                    curr_start_node, grid.shape, include_diagonals=False
                )

                for adjacent_position in adjacent_positions:
                    if grid[adjacent_position] != "#":
                        adjacent_garden_tile_lookup[curr_start_node].append(adjacent_position)

        outer_steps = {0: [start_node]}
        for idx in range(X_P1):
            next_steps = []
            for step in outer_steps[idx]:
                next_steps.extend(adjacent_garden_tile_lookup[step])

            outer_steps[idx + 1] = list(set(next_steps))  # Convert to set to remove duplicates

        return len(outer_steps[idx + 1])

    def part2(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        adjacent_garden_tile_lookup = {}
        start_node = (tuple([int(x) for x in np.where(grid == "S")]), (0, 0))

        # NOT POSSIBLE
        # for i in range(grid.shape[0]):
        #     for j in range(grid.shape[1]):
        #         curr_start_node = (i, j)
        #         adjacent_garden_tile_lookup[curr_start_node] = []
        #         adjacent_positions_and_maps = self.__get_adjacent_positions_and_maps(
        #             curr_start_node,
        #             grid.shape,
        #         )

        #         for adjacent_position, adjacent_map in adjacent_positions_and_maps:
        #             if grid[adjacent_position] != "#":
        #                 adjacent_garden_tile_lookup[curr_start_node].append(
        #                     (adjacent_position, adjacent_map)
        #                 )

        # curr_steps = [start_node]
        # for idx in range(X_P2):
        #     next_steps = []
        #     for step in curr_steps:
        #         for next_pos, map_modifier in adjacent_garden_tile_lookup[step]:
        #             next_map = (n1 + n2 for n1, n2 in zip(step[1], map_modifier))


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day21(day, use_sample, run_each)
    solver.solve()
