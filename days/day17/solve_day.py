from math import sqrt
from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions

TUPLES_TO_DIRECTIONS = {
    (-1, 0): "N",
    (1, 0): "S",
    (0, 1): "E",
    (0, -1): "W",
}

DIRECTIONS_TO_TUPLES = {y: x for x, y in TUPLES_TO_DIRECTIONS.items()}

DIST_BIAS = 0.1


class GridNode:
    def __init__(self, parent: Tuple = None, position: Tuple = None):
        self.parent = parent
        self.position = position

        self.path_cost = 0
        self.heuristic = 0
        self.total_cost = 0

        self.enter_direction = None
        if not parent is None:
            self.enter_direction = TUPLES_TO_DIRECTIONS[
                tuple([n1 - n2 for n1, n2 in zip(position, parent.position)])
            ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Node {self.position} - {self.enter_direction}, path cost {self.path_cost}, heuristic val {self.heuristic:0.2f} = {self.total_cost:0.2f}"

    def get_total_cost(self) -> float:
        self.total_cost = self.path_cost + self.heuristic

    def dist_to(self, pos: Tuple[int]) -> float:
        return sqrt(sum([(n1 - n2) ** 2 for n1, n2 in zip(self.position, pos)])) * DIST_BIAS


class Day17(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def pathfind_astar(
        self, grid: np.array, start_node: GridNode, goal_node: GridNode
    ) -> List[GridNode]:
        frontier = [start_node]
        explored = []

        while len(frontier) > 0:
            curr_node = frontier.pop(np.argmin([x.total_cost for x in frontier]))
            explored.append(curr_node)

            if curr_node.position == goal_node.position:
                path = []
                curr_node_backtrack = curr_node
                while curr_node_backtrack is not None:
                    path.append(curr_node_backtrack)
                    curr_node_backtrack = curr_node_backtrack.parent
                return path

            adjacent_positions = get_adjacent_positions(
                curr_node.position, grid.shape, include_diagonals=False
            )

            for pos in adjacent_positions:
                if curr_node.parent is not None:
                    if pos == curr_node.parent.position:
                        continue

                child_node = GridNode(curr_node, pos)

                already_explored = False
                for explored_node in explored:
                    if (
                        explored_node.position == child_node.position
                        and explored_node.enter_direction == child_node.enter_direction
                    ):
                        already_explored = True
                        break
                if already_explored:
                    continue

                child_node.path_cost = curr_node.path_cost + grid[child_node.position]
                child_node.heuristic = child_node.dist_to(goal_node.position)
                child_node.get_total_cost()

                better_path_cost = True
                for frontier_node in frontier:
                    if (
                        child_node.position == frontier_node.position
                        and child_node.path_cost > frontier_node.path_cost
                    ):
                        better_path_cost = False
                        break

                if not better_path_cost:
                    continue

                # Check if this is valid by following parents back in a line
                line_created = [child_node.parent]
                for _ in range(2):
                    next_parent = line_created[-1].parent
                    if next_parent is None:
                        break  # Not enough to draw a line

                    line_created.append(next_parent)

                line_too_long = False
                if len(line_created) == 3:
                    line_too_long = all(
                        [x.enter_direction == child_node.enter_direction for x in line_created]
                    )
                    if line_too_long:
                        continue

                frontier.append(child_node)
        raise ValueError("Did not find solution!")

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        grid = np.array(grid, dtype=int)
        goal_node = GridNode(None, (grid.shape[0] - 1, grid.shape[1] - 1))
        start_node = GridNode(None, (0, 0))

        full_path = self.pathfind_astar(grid, start_node, goal_node)
        for node in full_path:
            grid[node.position] = 0
        print(grid)
        return full_path[0].path_cost

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day17(day, use_sample, run_each)
    solver.solve()
