from enum import Enum, auto
from typing import List, Tuple

from solver import Solver


class ModuleType(Enum):
    FLIPFLOP = auto()
    CONJUNCTION = auto()
    BROADCAST = auto()
    OUTPUT = auto()
    ACTIVATOR = auto()


class SolvedException(Exception):
    pass


class Module:
    def __init__(self, module_spec: str) -> None:
        module_info, dests_info = module_spec.split(" -> ", maxsplit=1)

        if "%" in module_info:
            module_type = ModuleType.FLIPFLOP
        elif "&" in module_info:
            module_type = ModuleType.CONJUNCTION
        elif "broadcaster" in module_info:
            module_type = ModuleType.BROADCAST
        elif module_info == "rx":
            module_type = ModuleType.ACTIVATOR
        else:
            module_type = ModuleType.OUTPUT

        module_name = module_info.replace("%", "").replace("&", "")

        dests = [x for x in dests_info.split(", ") if x != ""]

        self.module_name = module_name
        self.module_type = module_type
        self.active = False
        self.input_connections = {}
        self.output_connections = dests

    def __str__(self) -> str:
        return (
            f"(Module: {self.module_name}, type {self.module_type},"
            f" outputting to {self.output_connections}, known_inputs: {list(self.input_connections.keys())}, active: {self.active})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def populate_inputs(self, all_modules: List["Module"]) -> None:
        if not self.module_type == ModuleType.CONJUNCTION:
            return

        for module in all_modules:
            if self.module_name in module.output_connections:
                self.input_connections[module.module_name] = False

    def get_state(self) -> bool:
        return self.active

    def handle_pulse(self, pulse_high: bool, pulse_from: str) -> List[Tuple[str, bool]]:
        match self.module_type:
            case ModuleType.FLIPFLOP:
                if pulse_high:
                    return []
                self.active = not self.active

            case ModuleType.CONJUNCTION:
                self.input_connections[pulse_from] = pulse_high
                self.active = not all(self.input_connections.values())

            case ModuleType.BROADCAST:
                self.active = False

            case ModuleType.OUTPUT:
                return []

            case ModuleType.ACTIVATOR:
                if not pulse_high:
                    raise SolvedException
                return []

        # return [(x, self.get_state, self.module_name) for x in self.output_connections]
        return [(x, self.active, self.module_name) for x in self.output_connections]


class Day20(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def return_false(self) -> bool:
        return False

    def __make_modules(self, data: List[str]) -> None:
        module_list = [Module(x) for x in data]
        module_names = set([x.module_name for x in module_list])

        missing_modules = []
        for module in module_list:
            module.populate_inputs(module_list)
            for output_module in module.output_connections:
                if output_module not in module_names:
                    missing_modules.append(f"{output_module} -> ")

        module_list.extend([Module(x) for x in missing_modules])
        self.modules = {x.module_name: x for x in module_list}

    def __get_next_instructions(self, instruction_list: List[Tuple]) -> List[Tuple]:
        high_pulse_count = 0
        low_pulse_count = 0
        curr_instruction = instruction_list.pop(0)
        curr_module_name, curr_pulse_method, from_module = curr_instruction
        curr_pulse = curr_pulse_method

        curr_module = self.modules[curr_module_name]
        if curr_pulse:
            high_pulse_count += 1
        else:
            low_pulse_count += 1
        return curr_module.handle_pulse(curr_pulse, from_module), high_pulse_count, low_pulse_count

    def part1(self, data: List[str]) -> None:
        self.__make_modules(data)

        button_pushes = 0
        high_pulse_count = 0
        low_pulse_count = 0

        for _ in range(1000):
            instruction_list = [("broadcaster", False, "button")]
            button_pushes += 1
            while len(instruction_list) > 0:
                next_instructions, high_pulses, low_pulses = self.__get_next_instructions(
                    instruction_list
                )
                instruction_list.extend(next_instructions)
                high_pulse_count += high_pulses
                low_pulse_count += low_pulses

        return high_pulse_count * low_pulse_count

    def part2(self, data: List[str]) -> None:
        self.__make_modules(data)

        button_pushes = 0
        high_pulse_count = 0
        low_pulse_count = 0

        while True:
            instruction_list = [("broadcaster", False, "button")]
            button_pushes += 1
            while len(instruction_list) > 0:
                try:
                    next_instructions, high_pulses, low_pulses = self.__get_next_instructions(
                        instruction_list
                    )
                except SolvedException:
                    return button_pushes
                instruction_list.extend(next_instructions)
                high_pulse_count += high_pulses
                low_pulse_count += low_pulses


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day20(day, use_sample, run_each)
    solver.solve()
