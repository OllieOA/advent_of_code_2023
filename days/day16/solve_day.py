from typing import List, Tuple

import numpy as np

from solver import Solver
from utils.parsers import NumpyArrayParser


class Day16(Solver):
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

        self.TURN_LEFT = {
            "N": "W",
            "W": "S",
            "S": "E",
            "E": "N",
        }

        self.TURN_RIGHT = {
            "N": "E",
            "E": "S",
            "S": "W",
            "W": "N",
        }

    def __simulate_grid(self, grid: np.array, starting_beam: Tuple[Tuple[int], str]) -> int:
        """The only trick here is that we cache beams - given it is fully
        deterministic, when a subsequent beams starts on an already explored
        path, we can ignore it as it will not energise any further tiles.
        """
        beams = [starting_beam]
        energised_tiles = set([])
        beam_cache = set([])
        while len(beams) > 0:
            next_beams = []
            for beam in beams:
                if beam in beam_cache:
                    continue  # Beam is die
                beam_cache.add(beam)
                beam_loc, beam_heading = beam
                energised_tiles.add(beam_loc)
                next_loc = tuple([n1 + n2 for n1, n2 in zip(beam_loc, beam_heading)])
                if not (
                    all([n >= 0 for n in next_loc])
                    and all([n < s for n, s in zip(next_loc, grid.shape)])
                ):
                    continue  # Beam is die

                next_symbol = grid[next_loc]
                match next_symbol:
                    case ".":
                        next_beams.append((next_loc, beam_heading))
                    case "-":
                        if beam_heading in [
                            self.DIRECTIONS_TO_TUPLES["E"],
                            self.DIRECTIONS_TO_TUPLES["W"],
                        ]:
                            next_beams.append((next_loc, beam_heading))
                        else:
                            next_beams.append((next_loc, self.DIRECTIONS_TO_TUPLES["E"]))
                            next_beams.append((next_loc, self.DIRECTIONS_TO_TUPLES["W"]))
                    case "|":
                        if beam_heading in [
                            self.DIRECTIONS_TO_TUPLES["N"],
                            self.DIRECTIONS_TO_TUPLES["S"],
                        ]:
                            next_beams.append((next_loc, beam_heading))
                        else:
                            next_beams.append((next_loc, self.DIRECTIONS_TO_TUPLES["N"]))
                            next_beams.append((next_loc, self.DIRECTIONS_TO_TUPLES["S"]))
                    case "/":
                        if beam_heading in [
                            self.DIRECTIONS_TO_TUPLES["N"],
                            self.DIRECTIONS_TO_TUPLES["S"],
                        ]:  # Turn right
                            next_beams.append(
                                (
                                    next_loc,
                                    self.DIRECTIONS_TO_TUPLES[
                                        self.TURN_RIGHT[self.TUPLES_TO_DIRECTIONS[beam_heading]]
                                    ],
                                )
                            )
                        else:  # Turn left
                            next_beams.append(
                                (
                                    next_loc,
                                    self.DIRECTIONS_TO_TUPLES[
                                        self.TURN_LEFT[self.TUPLES_TO_DIRECTIONS[beam_heading]]
                                    ],
                                )
                            )
                    case "\\":
                        if beam_heading in [
                            self.DIRECTIONS_TO_TUPLES["N"],
                            self.DIRECTIONS_TO_TUPLES["S"],
                        ]:  # Turn right
                            next_beams.append(
                                (
                                    next_loc,
                                    self.DIRECTIONS_TO_TUPLES[
                                        self.TURN_LEFT[self.TUPLES_TO_DIRECTIONS[beam_heading]]
                                    ],
                                )
                            )
                        else:  # Turn left
                            next_beams.append(
                                (
                                    next_loc,
                                    self.DIRECTIONS_TO_TUPLES[
                                        self.TURN_RIGHT[self.TUPLES_TO_DIRECTIONS[beam_heading]]
                                    ],
                                )
                            )
            beams = next_beams

        return len(energised_tiles) - 1

    def part1(self, data: List[str]) -> None:
        """Nothing major to explain - just implement the cases as described and
        simulate each beam."""
        grid = NumpyArrayParser(data).parse()
        start_beam = ((0, -1), self.DIRECTIONS_TO_TUPLES["E"])

        return self.__simulate_grid(grid, start_beam)

    def part2(self, data: List[str]) -> None:
        """We simply check all possible starts on the grid and get a solution
        quickly enough
        """
        grid = NumpyArrayParser(data).parse()

        all_starts = []
        for i in range(grid.shape[0]):
            all_starts.append(((i, -1), self.DIRECTIONS_TO_TUPLES["E"]))
            all_starts.append(((i, grid.shape[1]), self.DIRECTIONS_TO_TUPLES["W"]))

        for j in range(grid.shape[1]):
            all_starts.append(((-1, j), self.DIRECTIONS_TO_TUPLES["S"]))
            all_starts.append(((grid.shape[0], j), self.DIRECTIONS_TO_TUPLES["N"]))

        energized_results = []
        for start in all_starts:
            energized_results.append(self.__simulate_grid(grid, start))

        return max(energized_results)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day16(day, use_sample, run_each)
    solver.solve()
