import math

from typing import List, Tuple

from solver import Solver


class Day06(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __get_times_and_dists(self, data: List[str]):
        self.times = [int(x) for x in data[0].replace("Time:", "").split(" ") if x.isnumeric()]
        self.dists = [int(x) for x in data[1].replace("Distance:", "").split(" ") if x.isnumeric()]

    def __get_min_max_of_win_range(self, time: int, dist: int) -> Tuple[int]:
        """Simply go bottom-up and top-down until a win is identified"""
        min_time = -1
        curr_vel = 0
        while min_time < 0:
            curr_vel += 1
            t_remain = time - curr_vel
            if curr_vel * t_remain > dist:
                min_time = curr_vel

        max_time = -1
        curr_vel = time
        while max_time < 0:
            curr_vel -= 1
            t_remain = time - curr_vel
            if curr_vel * t_remain > dist:
                max_time = curr_vel

        return min_time, max_time

    def part1(self, data: List[str]) -> None:
        """We know that logically, there will be a min and max of a range
        in which winning is possible, and it is not possible outside it. As
        this is purely linear, there is no case in which the possibility to win
        is removed within the range. Therefore, we just need to find the min
        and max of this range of possibilities
        """
        self.__get_times_and_dists(data)
        num_wins = []

        for time, dist in zip(self.times, self.dists):
            min_time, max_time = self.__get_min_max_of_win_range(time, dist)
            num_wins.append(max_time - min_time + 1)

        return math.prod(num_wins)

    def part2(self, data: List[str]) -> None:
        """Do it again, but this is only reduced to one number. The algorithm
        is efficient enough
        """
        self.__get_times_and_dists(data)

        time = int("".join([str(x) for x in self.times]))
        dist = int("".join([str(x) for x in self.dists]))

        min_time, max_time = self.__get_min_max_of_win_range(time, dist)

        return max_time - min_time + 1


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day06(day, use_sample, run_each)
    solver.solve()
