import json
import re
from typing import List

from solver import Solver
from utils.parsers import NewLineListParser


class Part:
    def __init__(self, part_spec: str) -> None:
        for attribute in "xmas":
            part_spec = part_spec.replace(attribute, f'"{attribute}"')
        self.part_info = json.loads(part_spec.replace("=", ":"))

        self.active = True
        self.accepted = False
        self.curr_address = "in"

    def __str__(self) -> str:
        return "(" + ", ".join([f"{k}:{v}" for k, v in self.part_info.items()]) + ")"

    def __repr__(self) -> str:
        return self.__str__()

    def set_curr_address(self, new_address: str) -> None:
        if new_address in ["A", "R"]:
            self.active = False
            self.accepted = new_address == "A"
        self.curr_address = new_address

    def score(self) -> int:
        return sum(self.part_info.values()) if self.accepted else 0


class Workflow:
    def __init__(self, wf_spec: str) -> None:
        name, conditions = re.findall(r"(.*){(.*)}", wf_spec)[0]
        self.name = name

        self.conditions = []
        self.exit_address = ""

        # TODO: https://pastebin.com/XLzg3V9P
        self.next_cases = {
            "x": {},
            "m": {},
            "a": {},
            "s": {},
        }

        for cd in conditions.split(","):
            if ":" not in cd:
                self.exit_address = cd
                # if cd == "A":
                #     # Get all previous cases that are accepted
                #     pass
            test_condition, addr_if_true = cd.split(":")
            new_cd = {
                "attribute": test_condition[0],
                "eval_statement": f"n{test_condition[1:]}",
                "addr_if_true": addr_if_true,
            }
            self.conditions.append(new_cd)

    def parse_part(self, part: Part) -> None:
        for cd in self.conditions:
            addr_if_true = cd["addr_if_true"]
            eval_statement = cd["eval_statement"]

            test_val = part.part_info[cd["attribute"]]
            succeed_test = eval(eval_statement, {}, {"n": test_val})

            if succeed_test:
                break

        if succeed_test:
            part.set_curr_address(addr_if_true)
        else:
            part.set_curr_address(self.exit_address)

    def __str__(self) -> str:
        return f"Workflow {self.name}"

    def __repr__(self) -> str:
        return self.__str__()


class Day19(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def part1(self, data: List[str]) -> None:
        workflow_specs, part_specs = NewLineListParser(data).parse()
        parts = [Part(x) for x in part_specs]
        workflows = [Workflow(x) for x in workflow_specs]
        workflow_lookup = {x.name: x for x in workflows}

        for part in parts:
            while part.active:
                next_addr = part.curr_address
                workflow_lookup[next_addr].parse_part(part)

        return sum([p.score() for p in parts])

    def part2(self, data: List[str]) -> None:
        workflow_specs, _ = NewLineListParser(data).parse()
        workflows = [Workflow(x) for x in workflow_specs]
        workflow_lookup = {x.name: x for x in workflows}

        valid_ranges = {
            "x": [range(1, 4001)],
            "m": [range(1, 4001)],
            "a": [range(1, 4001)],
            "s": [range(1, 4001)],
        }

        test_cases = [("in", valid_ranges)]
        tested_cases = set([])

        while len(test_cases) > 0:
            pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day19(day, use_sample, run_each)
    solver.solve()
