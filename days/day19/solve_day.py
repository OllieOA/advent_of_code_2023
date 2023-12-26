import json
import math
import re
from typing import List

import networkx as nx

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
                break
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

        graph = nx.DiGraph()

        nodes = list(workflow_lookup.keys()) + ["A", "R"]

        graph.add_nodes_from(nodes)

        for workflow in workflows:
            opposite_conditions = []
            for condition in workflow.conditions:
                edge_if_true = (workflow.name, condition["addr_if_true"])
                true_edge_attributes = [
                    {
                        "part_type": condition["attribute"],
                        "condition": condition["eval_statement"][1],
                        "value": int(condition["eval_statement"][2:]),
                    }
                ]

                graph.add_edge(*edge_if_true, conditions=true_edge_attributes)

                if ">" in condition["eval_statement"]:
                    opposite_condition = "<="
                else:
                    opposite_condition = ">=" + condition["eval_statement"].replace("n<", "")

                val = int(condition["eval_statement"][2:])
                opposite_conditions.append(
                    {
                        "part_type": condition["attribute"],
                        "condition": opposite_condition,
                        "value": int(val),
                    }
                )
            graph.add_edge(*(workflow.name, workflow.exit_address), conditions=opposite_conditions)

        valid_ranges = {
            "x": [1, 4000],
            "m": [1, 4000],
            "a": [1, 4000],
            "s": [1, 4000],
        }

        all_edge_attr = nx.get_edge_attributes(graph, "conditions")

        all_paths_to_accepted = nx.all_simple_paths(graph, "in", "A")
        for path in all_paths_to_accepted:
            for edge_idx in range(len(path) - 1):
                curr_edge = (path[edge_idx], path[edge_idx + 1])
                edge_attrs = all_edge_attr[curr_edge]

                for edge_attr in edge_attrs:
                    attribute = edge_attr["part_type"]
                    condition = edge_attr["condition"]
                    val = edge_attr["value"]

                    if ">" in condition:
                        extra_offset = 0
                        if "=" in condition:
                            extra_offset = 1
                        next_val = val + extra_offset
                        if next_val >= valid_ranges[attribute][1]:
                            continue  # This is not a valid way to get to A
                        valid_ranges[attribute][0] = max(
                            valid_ranges[attribute][0], (val + extra_offset)
                        )
                    elif "<" in condition:
                        extra_offset = 0
                        if "=" in condition:
                            extra_offset = -1
                        next_val = val + extra_offset
                        if next_val <= valid_ranges[attribute][0]:
                            continue  # This is not a valid way to get to A
                        valid_ranges[attribute][1] = min(
                            valid_ranges[attribute][1], (val + extra_offset)
                        )
        # 3766094127300
        # 167409079868000
        return math.prod([y - x + 1 for x, y in valid_ranges.values()])

        # test_cases = ["in"]

        # while len(test_cases) > 0:
        #     # Determine the split based on the workflow
        #     curr_workflow = test_cases.pop(0)
        #     curr_exit_addr = workflow_lookup[curr_workflow].exit_address
        #     curr_conditions = workflow_lookup[curr_workflow].conditions

        #     for condition in curr_conditions:
        #         target_attr = condition["attribute"]

        #     print(workflow_lookup[curr_workflow].conditions, curr_exit_addr)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day19(day, use_sample, run_each)
    solver.solve()
