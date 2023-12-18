from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.grid_utils import get_adjacent_positions


class Day18(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.TUPLES_TO_DIRECTIONS = {(-1, 0): "U", (1, 0): "D", (0, 1): "R", (0, -1): "L"}
        self.DIRECTIONS_TO_TUPLES = {y: x for x, y in self.TUPLES_TO_DIRECTIONS.items()}
        self.HEX_SPEC_TO_DIRECTION = {"0": "R", "1": "D", "2": "L", "3": "U"}

    def is_in_grid(self, input_tuple: Tuple[int], grid_shape: Tuple[int]) -> bool:
        return (0 < input_tuple[0] < grid_shape[0]) and (0 < input_tuple[1] < grid_shape[1])

    def part1(self, data: List[str]) -> None:
        """We went for the naive solution because I thought the colours would be
        real and we would draw something pretty. Due to this, we construct the
        specified grid and flood fill it (similar to day 10). That will not work
        for part 2 so there is no need to refactor anything below.

        The grid is increased in size when required by concatenating, and then
        the flood fill works (after a padding) in such a way that gives us the
        sum.
        """
        grid = np.array([1], ndmin=2)
        curr_cell = (0, 0)
        for line in data:
            direction, dir_len_str, _ = line.split(" ")
            dir_len = int(dir_len_str)

            for _ in range(dir_len):
                next_cell = tuple(
                    [n1 + n2 for n1, n2 in zip(curr_cell, self.DIRECTIONS_TO_TUPLES[direction])]
                )
                if not self.is_in_grid(next_cell, grid.shape):
                    match direction:
                        case "U":
                            grid = np.vstack([np.zeros((1, grid.shape[1])), grid])
                            next_cell = (next_cell[0] + 1, next_cell[1])
                        case "D":
                            grid = np.vstack([grid, np.zeros((1, grid.shape[1]))])
                        case "L":
                            grid = np.hstack([np.zeros((grid.shape[0], 1)), grid])
                            # Correct for new offset
                            next_cell = (next_cell[0], next_cell[1] + 1)
                        case "R":
                            grid = np.hstack([grid, np.zeros((grid.shape[0], 1))])
                        case _:
                            raise ValueError(f"Cannot determine direction {direction}")
                grid[next_cell] = 1
                curr_cell = next_cell

        grid = np.pad(grid, pad_width=1, mode="constant")

        # Flood fill the grid with twos
        explored = set([])
        frontier = [(0, 0)]
        while len(frontier) > 0:
            next_node = frontier.pop()
            grid[next_node] = 2
            explored.add(next_node)
            neighbours = get_adjacent_positions(next_node, grid.shape)
            for neighour in neighbours:
                if grid[neighour] == 0:
                    frontier.append(neighour)

        grid[np.where(grid == 0)] = 1
        grid[np.where(grid == 2)] = 0
        return int(grid.sum())

    def part2(self, data: List[str]) -> None:
        """The area of a polygon with n known vertices is the sum of the
        multiple of the sum of the diffs between verticies. Why? I googled it,
        trusted it, implemented it, and it gave me the right answer. I had to
        compensate for the floor divide I think - not exactly sure why I was one
        off.
        """
        polygon_x = [0]
        polygon_y = [0]

        perimeter = 0
        for line in data:
            _, _, direction_spec = line.split(" ")

            direction_spec = direction_spec.replace("(#", "").replace(")", "")
            direction = self.HEX_SPEC_TO_DIRECTION[direction_spec[-1]]
            dist = int(direction_spec[:-1], 16)
            match direction:
                case "U":
                    polygon_x.append(polygon_x[-1])
                    polygon_y.append(polygon_y[-1] + dist)
                case "D":
                    polygon_x.append(polygon_x[-1])
                    polygon_y.append(polygon_y[-1] - dist)
                case "R":
                    polygon_x.append(polygon_x[-1] + dist)
                    polygon_y.append(polygon_y[-1])
                case "L":
                    polygon_x.append(polygon_x[-1] - dist)
                    polygon_y.append(polygon_y[-1])
                case _:
                    raise ValueError(f"Cannot determine direction {direction}")
            perimeter += dist
        area = 0
        j = -1

        for i in range(len(polygon_x) - 1):
            area += (polygon_x[j] + polygon_x[i]) * (polygon_y[j] - polygon_y[i])
            j = i
        return (area + perimeter) // 2 + 1  # +1 to compensate for floor divide


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day18(day, use_sample, run_each)
    solver.solve()
