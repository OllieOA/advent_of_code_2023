from itertools import combinations
import math
from typing import List, Tuple

from solver import Solver


class Hailstone:
    def __init__(self, idx: int, hailstone_spec: str) -> None:
        self.id = idx
        pos_spec, vel_spec = hailstone_spec.split(" @ ", maxsplit=2)

        self.start_pos_3d = tuple(int(x) for x in pos_spec.split(", "))
        self.vel_3d = tuple(int(x) for x in vel_spec.split(", "))

        self.start_pos_2d = tuple(x for x in self.start_pos_3d[:-1])
        self.vel_2d = tuple(x for x in self.vel_3d[:-1])

        # Get 2d equation of a line
        point_2 = tuple(n + v for n, v in zip(self.start_pos_2d, self.vel_2d))

        # m = (y2 - y1) / (x2 - x1)
        self.slope = float(point_2[1] - self.start_pos_2d[1]) / float(
            point_2[0] - self.start_pos_2d[0]
        )

        # b = y2 - (m * x2)
        self.y0 = point_2[1] - (self.slope * point_2[0])

        # Also get velocity normal vector for checking
        self.vel_vector = self.__get_normalised_vector_from_start(point_2)

    def __get_normalised_vector_from_start(self, point: Tuple[int]) -> Tuple[int]:
        point_len = math.sqrt(
            ((point[0] - self.start_pos_2d[0]) ** 2 + (point[1] - self.start_pos_2d[1]) ** 2)
        )
        if point_len == 0:
            return (None, None)
        normalised_vector = (
            (point[0] - self.start_pos_2d[0]) / point_len,
            point[1] - self.start_pos_2d[1] / point_len,
        )

        return normalised_vector

    def get_2d_intersection(self, other: "Hailstone") -> Tuple[int]:
        if other.slope == self.slope:
            return (None, None)  # Parallel
        x = (self.y0 - other.y0) / (other.slope - self.slope)
        y = self.slope * x + self.y0

        return (x, y)

    def check_if_point_in_past(self, point: Tuple[int]) -> bool:
        past_check_vector = self.__get_normalised_vector_from_start(point)
        return round(past_check_vector[0] / self.vel_vector[0]) < 0


class Day24(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        hailstones = [Hailstone(idx, line) for idx, line in enumerate(data)]
        hailstones_lookup = {x.id: x for x in hailstones}

        if self.use_sample:
            test_lim = (7, 27)
        else:
            test_lim = (200_000_000_000_000, 400_000_000_000_000)

        intersections = {}

        pairwise_hailstones = combinations(hailstones, 2)

        for a, b in pairwise_hailstones:
            intersections[(a.id, b.id)] = a.get_2d_intersection(b)

        intersect_within_test_area = 0
        for pair, intersection in intersections.items():
            if intersection[0] is None:
                continue  # Parallel

            # Check if intersection was not in either past
            past_intersections = [
                hailstones_lookup[h_id].check_if_point_in_past(intersection) for h_id in pair
            ]
            if any(past_intersections):
                continue

            if (
                test_lim[0] <= intersection[0] <= test_lim[1]
                and test_lim[0] <= intersection[1] <= test_lim[1]
            ):
                # Inside test limits
                intersect_within_test_area += 1

        return intersect_within_test_area

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day24(day, use_sample, run_each)
    solver.solve()
