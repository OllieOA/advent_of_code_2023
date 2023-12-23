from enum import Enum, auto
import math
from typing import List, Tuple

from solver import Solver


class ModuleType(Enum):
    FLIPFLOP = auto()
    CONJUNCTION = auto()
    BROADCAST = auto()
    OUTPUT = auto()


class Module:
    """This class has a couple of important properties.

    First, the module type, supported by the above enumerator (enums are great
    when you intend to use case statements. It is very readable).

    Then, we track the state of the module with a boolean, and we ensure we know
    the inputs/outputs. Outputs can be populated immediately, but we need to
    populate the inputs after we have constructed every module outside of a
    single instance.
    """

    def __init__(self, module_spec: str) -> None:
        module_info, dests_info = module_spec.split(" -> ", maxsplit=1)

        if "%" in module_info:
            module_type = ModuleType.FLIPFLOP
        elif "&" in module_info:
            module_type = ModuleType.CONJUNCTION
        elif "broadcaster" in module_info:
            module_type = ModuleType.BROADCAST
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
        """This helper function will populate a dict of inputs. For anything
        other than a conjuction module, we will just use the keys, but this
        dict will also be used to track the "memory" of the conjunction module.
        """
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

        return [(x, self.active, self.module_name) for x in self.output_connections]


class Day20(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def return_false(self) -> bool:
        return False

    def __make_modules(self, data: List[str]) -> None:
        """We make modules based on the instructions using the handy constructor
        and enum above. The one extra part is to populate "missing modules",
        which are realistically only the output (rx) module, given that the
        constructor assumes that the left side of the -> is the module name
        (which is not present for the output module).
        """
        module_list = [Module(x) for x in data]
        module_names = set([x.module_name for x in module_list])

        missing_modules = []
        for module in module_list:
            module.populate_inputs(module_list)
            for output_module in module.output_connections:
                if output_module not in module_names:
                    missing_modules.append(f"{output_module} -> ")

        missing_module_list = [Module(x) for x in missing_modules]

        module_list.extend(missing_module_list)
        for missing_module in missing_module_list:
            missing_module.populate_inputs(module_list)
        self.modules = {x.module_name: x for x in module_list}

    def __get_next_instructions(self, instruction_list: List[Tuple]) -> List[Tuple]:
        """We need to treat the instruction like a FIFO stack (i.e. a list)
        given the requirement to resolve instructions in order. Given part 1
        needs the pulse count, we need to output these separately, though this
        is not used in part 2.
        """
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
        """Simply populate and explore the queue after 1000 pushes (the pulse
        from the button push itself is already handled by considering the
        broadcaster as a normal module, but could equally be separated).
        """
        self.__make_modules(data)

        high_pulse_count = 0
        low_pulse_count = 0

        for _ in range(1000):
            instruction_list = [("broadcaster", False, "button")]
            while len(instruction_list) > 0:
                next_instructions, high_pulses, low_pulses = self.__get_next_instructions(
                    instruction_list
                )
                instruction_list.extend(next_instructions)
                high_pulse_count += high_pulses
                low_pulse_count += low_pulses

        return high_pulse_count * low_pulse_count

    def part2(self, data: List[str]) -> None:
        """This endeavours to be a general solution, but it was originally
        determined by inspecting the inputs.

        The method relies on recognising that there are four conjunction modules
        inputting to one conjunction that sends the low pulse to rx. These four
        modules can be assessed independently for when they output the required
        low signal, and then an LCM can be taken to determine the first loop in
        which they all line up, similar to previous problems.

        Given the confusing state tracking below, this function is heavily
        commented.
        """
        self.__make_modules(data)

        # Backpropagate from rx to find the necessary state of each combinator
        rx_input_module = self.modules[
            list(self.modules["rx"].input_connections.keys())[0]
        ]  # Requires a low pulse out, therefore all inputs must be high
        print(rx_input_module)

        """We know that all inputs to the rx_input_module are conjunctions from
        studying the input, and we know that they need to be high, so we need
        to assert that all inputs to the next layer out are low. Thankfully,
        there is only one input to each one at this level, and we can make the
        assertion that the NEXT level out is high. This is easier, because
        otherwise, we would need to support a branching tree structure.
        """

        # The following modules must have NOT all high inputs
        inputs_must_be_high_first_level = [x for x in rx_input_module.input_connections.keys()]

        inputs_must_be_low = []
        for high_in in inputs_must_be_high_first_level:
            inputs_must_be_low.append(list(self.modules[high_in].input_connections)[0])

        """Now we know that everything inputting to inputs_must_be_low must be
        high as they are all conjunction modules from inspection, (not asserted)
        """

        inputs_in_modules = {
            x: tuple(self.modules[x].input_connections.keys()) for x in inputs_must_be_low
        }
        presses_where_inputs_high = {x: -1 for x in inputs_must_be_low}
        button_pushes = 0

        """The only remaining step is to find the loops in which the inputs to
        each input group are all high at the same time, which would trigger the
        low state required. These inputs could be conjuctions or flipflops, it
        does not matter. Once we have found the earliest loop this happens for
        each, then we can just take the LCM and know the loop in which all 
        states align. "Loop" here refers to the outer button press loop.
        """

        while not all([x != -1 for x in presses_where_inputs_high.values()]):
            instruction_list = [("broadcaster", False, "button")]
            button_pushes += 1
            while len(instruction_list) > 0:
                next_instructions, _, _ = self.__get_next_instructions(instruction_list)
                instruction_list.extend(next_instructions)

                # Check the state of all the required groups
                for module_name, inputs_group in inputs_in_modules.items():
                    if not presses_where_inputs_high[module_name] == -1:
                        continue

                    input_states = [self.modules[x].active for x in inputs_group]
                    if all(input_states):
                        presses_where_inputs_high[module_name] = button_pushes

        return math.lcm(*list(presses_where_inputs_high.values()))


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day20(day, use_sample, run_each)
    solver.solve()
