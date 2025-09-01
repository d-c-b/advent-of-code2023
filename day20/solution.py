from os import path
from collections import defaultdict, deque
import itertools
import math


def parse_input() -> (
    tuple[
        dict[str, str],
        dict[str, list[str]],
    ]
):
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()

    module_types_map: dict[str, str] = {}
    destinations_map: dict[str, list[str]] = {}

    for line in lines:
        name_type, destinations_string = line.split(" -> ")
        destinations = destinations_string.split(", ")
        if name_type[0] in "%&":
            name, module_type = name_type[1:], name_type[0]
            module_types_map[name] = module_type

        else:
            name = name_type
            module_types_map[name] = ""
        destinations_map[name] = destinations

    return module_types_map, destinations_map


class ModuleTree:
    def __init__(
        self,
        module_types_map: dict[str, str],
        destinations_map: dict[str, list[str]],
    ) -> None:
        self.module_types_map = module_types_map
        self.destinations_map = destinations_map
        self.states_conjunctions: dict[str, dict[str, int]] = {}
        self.states_flip_flops: dict[str, bool] = {}
        self.sources_map: defaultdict[str, list[str]] = defaultdict(list)

        for name, destinations in destinations_map.items():
            for dest in destinations:
                self.sources_map[dest].append(name)

        for name, sources in self.sources_map.items():
            if module_types_map.get(name) == "%":
                self.states_flip_flops[name] = False

            elif module_types_map.get(name) == "&":
                self.states_conjunctions[name] = {source: False for source in sources}

    def reset_states(self) -> None:
        self.states_conjunctions = {
            conjunction_module: {source: False for source in states.keys()}
            for conjunction_module, states in self.states_conjunctions.items()
        }
        self.states_flip_flops = {
            flip_flop_module: False
            for flip_flop_module in self.states_flip_flops.keys()
        }

    def press_button(self) -> defaultdict[str, list[int]]:
        initial_state: list[tuple[str, str, int]] = [("button", "broadcaster", False)]
        pulses = deque(initial_state)

        sent_pulses: defaultdict[str, list[bool]] = defaultdict(list)

        while pulses:
            source, current, pulse_type = pulses.popleft()
            sent_pulses[current].append(pulse_type)

            if current not in self.module_types_map:
                continue
            current_module_type = self.module_types_map[current]
            match current_module_type:
                case "%":
                    if not pulse_type:
                        pulses.extend(
                            [
                                (
                                    current,
                                    destination,
                                    not self.states_flip_flops[current],
                                )
                                for destination in self.destinations_map[current]
                            ]
                        )

                        self.states_flip_flops[current] = not self.states_flip_flops[
                            current
                        ]

                case "&":
                    self.states_conjunctions[current][source] = pulse_type
                    pulses.extend(
                        [
                            (
                                current,
                                destination,
                                not all(self.states_conjunctions[current].values()),
                            )
                            for destination in self.destinations_map[current]
                        ]
                    )

                case _:
                    pulses.extend(
                        [
                            (current, destination, pulse_type)
                            for destination in self.destinations_map[current]
                        ]
                    )

        return sent_pulses

    def find_cycles_conjunction_module_low_pulses(self, module_name: str):
        self.reset_states()
        if self.module_types_map[module_name] != "&":
            raise Exception(
                f"Cannot find cycles for module {module_name}, must be a conjunction module"
            )

        low_pulse_sent_button_presses = []

        for i in itertools.count(1):
            sent_pulses = self.press_button()
            if False in sent_pulses[module_name]:
                low_pulse_sent_button_presses.append(i)

            if len(low_pulse_sent_button_presses) == 2:
                break

        first_occurrence, second_occurrence = low_pulse_sent_button_presses

        period = second_occurrence - first_occurrence
        offset = first_occurrence % period
        return period, offset


def solve_part_1() -> int:
    module_types_map, destinations_map = parse_input()
    low_count = 0
    high_count = 0

    modules = ModuleTree(module_types_map, destinations_map)
    for _ in range(1000):
        sent_pulses = modules.press_button()
        for pulses_sent in sent_pulses.values():
            low_count += pulses_sent.count(False)
            high_count += pulses_sent.count(True)

    return low_count * high_count


def solve_part_2() -> int:
    TARGET_MODULE = "rx"
    module_types_map, destinations_map = parse_input()
    modules = ModuleTree(module_types_map, destinations_map)
    sources_for_target_module = modules.sources_map[TARGET_MODULE]

    # Based on input, there is exactly one source module for the target module, which is a conjunction
    assert len(sources_for_target_module) == 1
    source_module_to_check = sources_for_target_module[0]
    assert source_module_to_check in modules.states_conjunctions

    # Also make assumption all of the inputs to this are also conjunctions
    assert all(
        [
            module in modules.states_conjunctions
            for module in modules.sources_map[source_module_to_check]
        ]
    )

    periods_to_match = []
    offsets = []
    for conjunction_source in modules.sources_map[source_module_to_check]:
        period, offset = modules.find_cycles_conjunction_module_low_pulses(
            conjunction_source
        )
        periods_to_match.append(period)
        offsets.append(offset)

    # Finally assert all offsets are 0 so can use a simple LCM  for answer
    assert all([offset == 0 for offset in offsets])

    return math.lcm(*periods_to_match)


print(
    f"""
    Day 20: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
