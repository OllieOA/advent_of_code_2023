from copy import deepcopy
from typing import List, Tuple, Dict

from solver import Solver

ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Brick:
    def __init__(self, start_coord: str, end_coord: str, idx: int) -> None:
        self.coords = []
        self.start_coord = tuple([int(x) for x in start_coord.split(",")])
        self.end_coord = tuple([int(x) for x in end_coord.split(",")])
        self.height = abs(self.start_coord[2] - self.end_coord[2]) + 1
        self.id = idx
        self.supported_by = set([])

        for i in range(self.start_coord[0], self.end_coord[0] + 1):
            for j in range(self.start_coord[1], self.end_coord[1] + 1):
                for k in range(self.start_coord[2], self.end_coord[2] + 1):
                    self.coords.append((i, j, k))

        self.active = True
        self.z_pos = min(self.start_coord[2], self.end_coord[2] + 1)
        self.coords_2d = set([(x, y) for x, y, z in self.coords])

        # CONFIRMED - No diagonal (i.e. line) bricks
        # if sum([int((x1 - x2) > 0) for x1, x2 in zip(self.end_coord, self.start_coord)]) > 2:
        #     print(f"DIAGONAL BRICK!")

    def __lt__(self, other: "Brick") -> bool:
        return self.z_pos < other.z_pos

    def __str__(self) -> str:
        return f"b{self.id}:{self.coords[0]}~{self.coords[-1]}, h{self.height}"

    def __repr__(self) -> str:
        return self.__str__()

    def settle(self, lowest_point_available_map: Dict, bricks_by_level: Dict) -> None:
        curr_settle_level = 0
        for coord_2d in list(self.coords_2d):
            curr_settle_level = max(curr_settle_level, lowest_point_available_map.get(coord_2d, 0))

        drop_magnitude = self.z_pos - curr_settle_level - 1
        self.z_pos = curr_settle_level + self.height
        self.coords = [(x, y, z - drop_magnitude) for x, y, z in self.coords]
        self.min_point = min([x[-1] for x in self.coords])
        self.max_point = max([x[-1] for x in self.coords])

        for coord_2d in list(self.coords_2d):
            lowest_point_available_map[coord_2d] = curr_settle_level + self.height

        for coord in self.coords:
            if coord[-1] not in bricks_by_level:
                bricks_by_level[coord[-1]] = set([])
            bricks_by_level[coord[-1]].add(self.id)


class Day22(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __make_and_settle_bricks(self, data: List[str]) -> None:
        bricks = sorted([Brick(*x.split("~"), idx) for idx, x in enumerate(data)])
        brick_lookup = {x.id: x for x in bricks}

        # Settle all the bricks to the lowest point
        lowest_point_available_map = {}  # Initialise
        bricks_at_level = {}
        for brick in bricks:
            brick.settle(lowest_point_available_map, bricks_at_level)

        # Find any bricks that are being supported and append
        for brick in bricks:
            possible_bricks_below = bricks_at_level.get(brick.min_point - 1, [])
            for possible_below_brick in possible_bricks_below:
                if (
                    len(brick.coords_2d.intersection(brick_lookup[possible_below_brick].coords_2d))
                    > 0
                ):
                    brick.supported_by.add(possible_below_brick)

        self.bricks = bricks

    def part1(self, data: List[str]) -> None:
        self.__make_and_settle_bricks(data)
        cannot_disintegrate = set([])

        for brick in self.bricks:
            if len(brick.supported_by) == 1:
                cannot_disintegrate.add(list(brick.supported_by)[0])

        return len(self.bricks) - len(cannot_disintegrate)

    def part2(self, data: List[str]) -> None:
        self.__make_and_settle_bricks(data)
        fall_results = {}

        for brick in self.bricks:
            fall_results[brick.id] = 0
            fallen = {x.id: False for x in self.bricks}
            fallen[brick.id] = True
            supported_by_ref = {x.id: deepcopy(x.supported_by) for x in self.bricks}

            some_fallen = True
            while some_fallen:
                some_fallen = False
                mark_for_removal = {}

                # Check if there are any supports that need to be removed
                for brick_id, supports in supported_by_ref.items():
                    for support in supports:
                        if fallen[support]:
                            if brick_id not in mark_for_removal:
                                mark_for_removal[brick_id] = set([])
                            mark_for_removal[brick_id].add(support)

                for brick_id, removal_set in mark_for_removal.items():
                    supported_by_ref[brick_id] = supported_by_ref[brick_id].difference(removal_set)

                    if len(supported_by_ref[brick_id]) == 0 and not fallen[brick_id]:
                        fallen[brick_id] = True
                        some_fallen = True

            fall_results[brick.id] += sum(fallen.values()) - 1

        return sum(fall_results.values())


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day22(day, use_sample, run_each)
    solver.solve()
