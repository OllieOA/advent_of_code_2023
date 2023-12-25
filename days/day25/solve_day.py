from itertools import combinations
from typing import List

import networkx as nx
import matplotlib.pyplot as plt

from solver import Solver


class Day25(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        """networkx totally trivialised this problem, as there is a function
        within the flow algorithms that calculate the minimum cuts required to
        separate a flow between two nodes, and it is very fast. Just do so until
        we have two groups split by 3 cuts."""
        graph = nx.Graph()

        for line in data:
            root_node, other_nodes = line.split(": ")
            other_nodes = [x for x in other_nodes.split(" ")]
            connections = [(root_node, x) for x in other_nodes]

            for node in [root_node] + other_nodes:
                graph.add_node(node)

            for connection in connections:
                graph.add_edge(*connection, capacity=1)

        for node_pair in combinations(graph.nodes, 2):
            min_cut, groups = nx.minimum_cut(graph, *node_pair)
            if min_cut == 3:
                group1, group2 = groups
                return len(group1) * len(group2)

    def part2(self, _data: List[str]) -> None:
        print("mery crimbas")


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day25(day, use_sample, run_each)
    solver.solve()
