import argparse
import importlib
import logging
from pathlib import Path
import time
from typing import List, Callable

from utils.data_loader import DataLoader

_LOG_FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_LOG = logging.getLogger(__name__)

_LOG_STREAM_HANDLER = logging.StreamHandler()
_LOG_STREAM_HANDLER.setFormatter(_LOG_FORMATTER)

_LOG.addHandler(_LOG_STREAM_HANDLER)
_LOG.setLevel(logging.DEBUG)


class Solver:
    def __init__(self, use_sample: bool, run_each: List[bool]) -> None:
        self.use_sample = use_sample
        self.my_base_path = __file__
        self.day = -1
        self.logger = _LOG
        self.run_part1, self.run_part2 = run_each

    def part1(self, data: List) -> None:
        raise NotImplementedError("Implement this method in a child class!")

    def part2(self, data: List) -> None:
        raise NotImplementedError("Implement this method in a child class!")

    def _solve(self, solver: Callable, part: int, use_sample: bool) -> None:
        start_time = time.time()
        _LOG.info(f"| Part {part} | File I/O |")
        if use_sample:
            target_file = Path(self.my_base_path).parent / f"p{part}_sample.txt"
            alt_file = Path(self.my_base_path).parent / f"sample.txt"
        else:
            target_file = Path(self.my_base_path).parent / f"p{part}_input.txt"
            alt_file = Path(self.my_base_path).parent / f"input.txt"

        if not target_file.exists():
            if alt_file.exists():
                target_file = alt_file  # Used when the input does not change from part 1 to 2
            else:
                raise FileNotFoundError("Could not find a suitable input!")

        data = DataLoader(target_file).load_data()

        _LOG.info(f"| Part {part} | Solving |")
        result = solver(data)
        end_time = time.time()
        _LOG.info(f"| Solved! Answer: {result} in {(end_time-start_time) * 1000: 0.3f} ms!")

    def solve(self):
        _LOG.info(f"| =------= DAY {self.day:02d} =------= |")
        if self.run_part1:
            self._solve(self.part1, 1, self.use_sample)
        if self.run_part2:
            self._solve(self.part2, 2, self.use_sample)
        _LOG.info(f"| =-----= COMPLETE =-----= |")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("d", type=int, help="Day to run (integer)")
    args.add_argument("-s", action="store_true", help="Run with sample input")
    args.add_argument("-a", action="store_true", help="Run all days")
    args.add_argument("-o1", action="store_true", help="Only run day 1")
    args.add_argument("-o2", action="store_true", help="Only run day 2")

    opts = args.parse_args()
    if opts.o1 and opts.o2:
        _LOG.error("Don't specify both days to run!")

    run_each = [opts.o1, opts.o2]
    if not any(run_each):
        run_each = [True, True]

    if opts.a:
        days = range(1, 26)
    else:
        days = [opts.d]

    for day in days:
        try:
            day_solver = importlib.import_module(f"days.day{day:02d}.solve_day")
            day_solver.solve_day(day, opts.s, run_each)
        except ImportError:
            _LOG.error(f"!!! DAY {day:02d} NOT IMPLEMENTED YET !!!")
