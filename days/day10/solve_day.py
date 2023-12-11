from collections import Counter
from typing import List

import numpy as np

from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions
from solver import Solver


class Day10(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day
        self.CONNECTIONS = {
            "|": ["N", "S"],
            "-": ["E", "W"],
            "L": ["N", "E"],
            "J": ["N", "W"],
            "7": ["S", "W"],
            "F": ["S", "E"],
        }

        self.TUPLES_TO_DIRECTIONS = {
            (-1, 0): "N",
            (1, 0): "S",
            (0, 1): "E",
            (0, -1): "W",
        }

        self.DIRECTIONS_TO_TUPLES = {y: x for x, y in self.TUPLES_TO_DIRECTIONS.items()}

        self.OPPOSITES = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __make_loop(self, grid: np.array) -> None:
        """Here, we consider each adjacent node as a start point and then
        attempt to construct the loop. If we find our way back to the start node
        we can assume the loop is complete, and then half the amount of nodes.

        There is some luck with the input checking order here, because we are
        not excluding the case where the first adjacent node does not connect
        to the start node - these SHOULD be excluded.
        """
        start_node = tuple([int(x) for x in np.where(grid == "S")])

        # Set up loops - each loop will start from the first node and continue
        # evaluating until the loop is closed or not possible to close

        final_connecting_nodes = [
            x for x in get_adjacent_positions(start_node, grid.shape, include_diagonals=False)
        ]

        for loop_start in final_connecting_nodes:
            loop = [start_node, loop_start]

            connected = False  # True when the last node is start node
            while not connected:
                direction_facing_tuple = tuple(x - y for x, y in zip(loop[-1], loop[-2]))
                direction_facing_name = self.TUPLES_TO_DIRECTIONS[direction_facing_tuple]

                connections_available_at_node = self.CONNECTIONS[grid[loop[-1]]]

                entered_from = self.OPPOSITES[direction_facing_name]

                if not entered_from in connections_available_at_node:
                    # Not connected to this pipe
                    break
                connections_identified = [
                    x for x in self.CONNECTIONS[grid[loop[-1]]] if x != entered_from
                ]
                assert len(connections_identified) == 1, "Too many connections - check logic"

                connection_available = connections_identified[0]
                new_dir = self.DIRECTIONS_TO_TUPLES[connection_available]

                new_node = (loop[-1][0] + new_dir[0], loop[-1][1] + new_dir[1])

                if (
                    new_node[0] < 0
                    or new_node[0] >= grid.shape[0]
                    or new_node[1] < 0
                    or new_node[1] >= grid.shape[1]
                ):
                    # Off the board
                    break

                if grid[new_node] == ".":
                    # Ground tile
                    break

                loop.append(new_node)
                connected = grid[new_node] == "S"

            if not connected:
                # If we have gotten here from a break, we need to try a new loop
                continue

        self.loop = loop

    def part1(self, data: List[str]) -> None:
        self.grid = NumpyArrayParser(data).parse()
        self.__make_loop(self.grid)

        return (len(self.loop) - 1) // 2

    def part2(self, _data: List[str]) -> None:
        """The tricky part here is that we need to consider the possibility
        where there are two pipes side by side, e.g. ||, which STILL encloses
        a loop.

        This is a great case for a flood-fill approach, but to do this, we need
        to expand the grid to allow for the flooding. In this case, we expand
        each grid element to a 3x3 grid element (2x2 is possible, but 3x3 is
        intuitively easier)

        Another trick is that I do not want to know the "S" direction, so I just
        assume all directions so we can make the "wall" of the expanded grid.
        This will not affect us as they will not come into the final calculation
        """
        big_grid = np.ones((3 * self.grid.shape[0], 3 * self.grid.shape[1]), dtype=str)
        big_grid[big_grid == "1"] = "."
        big_loop = [tuple([3 * i for i in c]) for c in self.loop]

        for big_pipe_coord, little_pipe_coord in zip(big_loop, self.loop):
            big_grid[big_pipe_coord] = self.grid[little_pipe_coord]

            if self.grid[little_pipe_coord] == "S":
                for coord in get_adjacent_positions(
                    big_pipe_coord, big_grid.shape, include_diagonals=False
                ):
                    big_grid[coord] = "#"
                continue

            dirs = self.CONNECTIONS[self.grid[little_pipe_coord]]
            for each_dir in dirs:
                dir_tuple = self.DIRECTIONS_TO_TUPLES[each_dir]
                big_grid[big_pipe_coord[0] + dir_tuple[0], big_pipe_coord[1] + dir_tuple[1]] = "#"

        # Get all of the outside edges - we will use them as starting points for
        # a flood fill
        outside_edges = [(0, y) for y in range(big_grid.shape[1])]
        outside_edges += [(big_grid.shape[0] - 1, y) for y in range(big_grid.shape[1])]
        outside_edges += [(x, 0) for x in range(big_grid.shape[0])]
        outside_edges += [(x, big_grid.shape[1] - 1) for x in range(big_grid.shape[0])]

        outside_edges = [c for c in outside_edges if big_grid[c] == "."]

        out_of_loop = set([])
        for start_fill in outside_edges:
            if start_fill in out_of_loop:
                continue
            frontier = [start_fill]
            while len(frontier) > 0:
                next_node = frontier.pop(0)
                out_of_loop.add(next_node)
                neighbours = get_adjacent_positions(next_node, big_grid.shape)
                for neighbour in neighbours:
                    if neighbour in out_of_loop or neighbour in frontier:
                        continue
                    if big_grid[neighbour] == ".":
                        frontier.append(neighbour)

        for ool in list(out_of_loop):
            big_grid[ool] = "X"

        total_enclosed = 0
        counted = 0
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if big_grid[3 * i, 3 * j] == ".":
                    total_enclosed += 1

                big_grid[3 * i, 3 * j] = counted
                counted += 1

        return total_enclosed


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day10(day, use_sample, run_each)
    solver.solve()
