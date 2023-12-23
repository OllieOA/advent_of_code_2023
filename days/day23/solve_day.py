from queue import PriorityQueue
from typing import List, Tuple

import networkx as nx

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser
from utils.grid_utils import get_adjacent_positions


class GridNode:
    def __init__(self, parent: Tuple = None, position: Tuple = None, path_cost: int = 0):
        self.parent = parent
        self.position = position

        self.path_cost = path_cost

        self.enter_direction = None
        if not parent is None:
            self.enter_direction = (
                position[0] - parent.position[0],
                position[1] - parent.position[1],
            )

        self.explored_mark = f"{self.position}"

    def __eq__(self, other: object) -> bool:
        self.explored_mark == other.explored_mark

    def __lt__(self, other):
        return self.path_cost < other.path_cost


class Day23(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.TUPLES_TO_DIRECTIONS = {
            (-1, 0): "N",
            (1, 0): "S",
            (0, 1): "E",
            (0, -1): "W",
        }

        self.DIRECTIONS_TO_TUPLES = {y: x for x, y in self.TUPLES_TO_DIRECTIONS.items()}

    def __is_intersection(self, node: Tuple[int], grid: np.array) -> bool:
        if grid[node] != ".":
            return False
        adjacent_nodes = get_adjacent_positions(node, grid.shape, include_diagonals=False)
        steppable = sum([int(grid[x] != "#") for x in adjacent_nodes])

        return steppable > 2

    def __find_intersection_map(
        self, grid: np.array, start_node: Tuple[int], goal_node: Tuple[int]
    ):
        # Find all intersections and find all paths (and lengths) to next
        # available intersections

        intersections = set([start_node, goal_node])

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                curr_node = (i, j)
                if grid[curr_node] != ".":
                    continue

                if curr_node in intersections:
                    continue

                if self.__is_intersection(curr_node, grid):
                    intersections.add(curr_node)

        self.intersections = intersections

        intersection_map = {}

        for intersection in list(intersections):
            frontier = [GridNode(None, intersection)]
            explored = set([])
            while len(frontier) > 0:
                curr_step = frontier.pop(0)
                explored.add(curr_step.position)

                candidates = [
                    GridNode(curr_step, x, curr_step.path_cost + 1)
                    for x in get_adjacent_positions(
                        curr_step.position, grid.shape, include_diagonals=False
                    )
                ]

                for candidate in candidates:
                    if candidate.position in explored:
                        continue

                    if candidate.position in intersections:
                        intersection_map[(intersection, candidate.position)] = candidate.path_cost
                        continue

                    cell_type = grid[candidate.position]
                    if cell_type == "#":
                        continue

                    if cell_type == ".":
                        frontier.append(candidate)
                        continue

                    # If not, we need to check if it is traversable
                    if (
                        cell_type == "v"
                        and self.TUPLES_TO_DIRECTIONS[candidate.enter_direction] != "S"
                    ):
                        continue
                    elif (
                        cell_type == "<"
                        and self.TUPLES_TO_DIRECTIONS[candidate.enter_direction] != "W"
                    ):
                        continue
                    elif (
                        cell_type == ">"
                        and self.TUPLES_TO_DIRECTIONS[candidate.enter_direction] != "E"
                    ):
                        continue
                    elif (
                        cell_type == "^"
                        and self.TUPLES_TO_DIRECTIONS[candidate.enter_direction] != "N"
                    ):
                        continue
                    else:
                        frontier.append(candidate)

        self.intersection_map = intersection_map

    def __make_graph(self) -> None:
        self.graph = nx.DiGraph()

        self.nodes = {n: idx for idx, n in enumerate(list(self.intersections))}
        self.nodes_lookup = {y: x for x, y in self.nodes.items()}

        self.graph.add_nodes_from(self.nodes.values())

        for edge_spec, cost in self.intersection_map.items():
            edge = (self.nodes[e] for e in edge_spec)
            self.graph.add_edge(*edge, weight=cost)

    def __solve_graph(self, start_node, goal_node) -> int:
        max_len = 0
        for path in nx.all_simple_paths(
            self.graph, source=self.nodes[start_node], target=self.nodes[goal_node]
        ):
            total_len = 0
            for idx in range(len(path) - 1):
                total_len += self.intersection_map[
                    (self.nodes_lookup[path[idx]], self.nodes_lookup[path[idx + 1]])
                ]
            max_len = max(max_len, total_len)

        return max_len

    def part1(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()

        start_node = (0, 1)
        goal_node = (grid.shape[0] - 1, grid.shape[1] - 2)

        self.__find_intersection_map(grid, start_node, goal_node)
        self.__make_graph()
        return self.__solve_graph(start_node, goal_node)

    def part2(self, data: List[str]) -> None:
        grid = NumpyArrayParser(data).parse()
        grid[grid == "^"] = "."
        grid[grid == ">"] = "."
        grid[grid == "<"] = "."
        grid[grid == "v"] = "."

        start_node = (0, 1)
        goal_node = (grid.shape[0] - 1, grid.shape[1] - 2)

        self.__find_intersection_map(grid, start_node, goal_node)
        self.__make_graph()
        return self.__solve_graph(start_node, goal_node)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day23(day, use_sample, run_each)
    solver.solve()
