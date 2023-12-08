from os import path
import itertools
import math
from collections import Counter, defaultdict
from typing import Callable


def parse_input() -> tuple[str, dict[str, dict[str, str]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    instruction_list, map_links = input_file.read().strip().split("\n\n")

    mapping_links = dict()

    for map_link in map_links.splitlines():
        key, left_right_paths_string = map_link.split(" = ")
        mapping_links[key] = {
            key: val
            for key, val in zip(
                ("L", "R"), left_right_paths_string.strip("()").split(", ")
            )
        }

    return instruction_list, mapping_links


def find_prime_factors(number: int) -> list[int]:
    prime_factors = []
    for i in range(2, math.ceil(number ** (1 / 2))):
        while number % i == 0:
            prime_factors.append(i)
            number = number // i
    prime_factors.append(number)
    return prime_factors


def lcm(numbers: list[int]) -> int:
    prime_factor_counts: defaultdict[int, int] = defaultdict(int)
    for n in numbers:
        prime_factors = find_prime_factors(n)
        counts = Counter(prime_factors)
        for factor in counts:
            prime_factor_counts[factor] = max(
                counts[factor], prime_factor_counts[factor]
            )
    return math.prod([val * count for val, count in prime_factor_counts.items()])


def number_of_steps_to_end_point(
    position: str,
    instruction_list: str,
    map_links: dict[str, dict[str, str]],
    break_condition: Callable[[str], bool],
) -> int:
    for i in itertools.count():
        instruction = instruction_list[i % len(instruction_list)]
        position = map_links[position][instruction]

        if break_condition(position):
            break

    return i + 1


def solve_part_1() -> int:
    instruction_list, map_links = parse_input()
    return number_of_steps_to_end_point(
        "AAA", instruction_list, map_links, lambda x: x == "ZZZ"
    )


def solve_part_2() -> int:
    instruction_list, map_links = parse_input()
    starting = [position for position in map_links if position.endswith("A")]
    return lcm(
        [
            number_of_steps_to_end_point(
                start_position, instruction_list, map_links, lambda x: x.endswith("Z")
            )
            for start_position in starting
        ]
    )


print(
    f"""
    Day 08: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
