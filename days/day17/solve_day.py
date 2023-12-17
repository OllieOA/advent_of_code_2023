from queue import PriorityQueue
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions


class GridNode:
    """This is just a data object which tracks the unique things required for a
    priority queue. We use an "explored_mark" to cache which is just a string
    jammed together with the properties which can also be used as __eq__, and a
    __lt__ method is needed for the priority queue.
    """

    def __init__(self, parent: Tuple = None, position: Tuple = None):
        self.parent = parent
        self.position = position

        self.path_cost = 0
        self.straight_path_num = 0

        self.enter_direction = None
        if not parent is None:
            self.enter_direction = (
                position[0] - parent.position[0],
                position[1] - parent.position[1],
            )

            if self.enter_direction == self.parent.enter_direction:
                self.straight_path_num = self.parent.straight_path_num + 1

        self.explored_mark = f"{self.position}{self.enter_direction}{self.straight_path_num}"

    def __eq__(self, other: object) -> bool:
        self.explored_mark == other.explored_mark

    def __lt__(self, other):
        return self.path_cost < other.path_cost


class Day17(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def pathfind_astar(
        self,
        grid: np.array,
        start_node: GridNode,
        goal_node: GridNode,
        max_straight: int,
        min_before_turn: int,
    ) -> GridNode:
        """This was originally called astar because it implemented A*, but I
        found no real benefit in the heuristic for this work, so it turned into
        Dijkstra's.
        """
        frontier = PriorityQueue()
        frontier.put((0, start_node))
        dists = {start_node.explored_mark: 0}

        loop_idx = -1

        while not frontier.empty():
            loop_idx += 1
            path_cost, curr_node = frontier.get()
            if loop_idx % 10000 == 0:
                print(
                    f"\t{abs(curr_node.position[0] - goal_node.position[0]) + abs(curr_node.position[1] - goal_node.position[1]):.0f} away...",
                    end="\r",
                )

            if curr_node.position == goal_node.position:
                # return curr_node
                path = []
                curr_node_backtrack = curr_node
                while curr_node_backtrack is not None:
                    path.append(curr_node_backtrack)
                    curr_node_backtrack = curr_node_backtrack.parent
                return path

            if path_cost > dists[curr_node.explored_mark]:
                continue

            if curr_node.straight_path_num < (min_before_turn - 1) and curr_node.parent is not None:
                adjacent_positions = get_adjacent_positions(
                    curr_node.position,
                    grid.shape,
                    include_diagonals=False,
                    direction=curr_node.enter_direction,
                )
            else:
                adjacent_positions = get_adjacent_positions(
                    curr_node.position, grid.shape, include_diagonals=False
                )

            for pos in adjacent_positions:
                if curr_node.parent is not None:
                    if pos == curr_node.parent.position:
                        continue  # Walked back into the same square

                child_node = GridNode(curr_node, pos)

                if child_node.straight_path_num >= max_straight:
                    continue

                child_node.path_cost = curr_node.path_cost + grid[pos]

                if (
                    child_node.explored_mark in dists
                    and dists[child_node.explored_mark] <= child_node.path_cost
                ):
                    continue
                dists[child_node.explored_mark] = child_node.path_cost

                frontier.put((child_node.path_cost, child_node))

        raise ValueError("Did not find solution!")

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        grid = np.array(grid, dtype=int)
        goal_node = GridNode(None, (grid.shape[0] - 1, grid.shape[1] - 1))
        start_node = GridNode(None, (0, 0))

        last_node = self.pathfind_astar(
            grid, start_node, goal_node, max_straight=3, min_before_turn=0
        )
        return last_node.path_cost

    def part2(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        grid = np.array(grid, dtype=int)
        goal_node = GridNode(None, (grid.shape[0] - 1, grid.shape[1] - 1))
        start_node = GridNode(None, (0, 0))

        last_node = self.pathfind_astar(
            grid, start_node, goal_node, max_straight=10, min_before_turn=4
        )
        return last_node.path_cost


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day17(day, use_sample, run_each)
    solver.solve()
