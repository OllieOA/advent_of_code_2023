from copy import deepcopy
from typing import List

from solver import Solver


class Day09(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __make_sequences_histories(self, sequences: List[List[int]]) -> None:
        """Generate the sequence histories as per the specification.
        This just steps through the algorithm for each line until all
        0's are encountered. The only trick here is, for convenience, we
        stack it such that the smallest sequence (all 0s) is at the
        first index of the list, so we don't need to bother literally
        reversing the index when we "go back up" the structure.
        """
        all_stepped_sequences = []
        for sequence in sequences:
            sequence_steps = [sequence]

            while any([n != 0 for n in sequence_steps[0]]):
                next_seq = []
                for idx in range(len(sequence_steps[0]) - 1):
                    next_seq.append(sequence_steps[0][idx + 1] - sequence_steps[0][idx])

                sequence_steps = [next_seq] + sequence_steps

            all_stepped_sequences.append(sequence_steps)

        self.all_stepped_sequences = all_stepped_sequences

    def __solve_sequences_end_history(self, sequence_steps) -> int:
        """Given the trick, we just need to initialise a new 0 value,
        and then step through the arithmetic in the order.
        """
        sequence_steps[0].append(0)

        for idx in range(len(sequence_steps) - 1):
            sequence_steps[idx + 1].append(sequence_steps[idx + 1][-1] + sequence_steps[idx][-1])

        return sequence_steps[-1][-1]

    def __solve_sequences_start_history(self, sequence_steps) -> int:
        """Same as above, though we need to change the way we construct
        the next layer to start with the value, but otherwise the logic
        is the same.
        """
        sequence_steps[0].append(0)

        for idx in range(len(sequence_steps) - 1):
            sequence_steps[idx + 1] = [
                sequence_steps[idx + 1][0] - sequence_steps[idx][0]
            ] + sequence_steps[idx + 1]

        return sequence_steps[-1][0]

    def part1(self, data: List[str]) -> None:
        sequences = [[int(x) for x in line.split(" ")] for line in data]
        self.__make_sequences_histories(sequences)

        all_stepped_sequences = deepcopy(self.all_stepped_sequences)
        sequence_solutions = [self.__solve_sequences_end_history(s) for s in all_stepped_sequences]

        return sum(sequence_solutions)

    def part2(self, data: List[str]) -> None:
        sequences = [[int(x) for x in line.split(" ")] for line in data]
        self.__make_sequences_histories(sequences)

        all_stepped_sequences = deepcopy(self.all_stepped_sequences)
        sequence_solutions = [
            self.__solve_sequences_start_history(s) for s in all_stepped_sequences
        ]

        return sum(sequence_solutions)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day09(day, use_sample, run_each)
    solver.solve()
