from os import path
from collections import defaultdict


def parse_input() -> list[str]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    return [word for line in lines for word in line.split(",")]


def run_hash_algorithm(string: str) -> int:
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val %= 256
    return val


def solve_part_1() -> int:
    initialisation_sequence = parse_input()
    vals = [run_hash_algorithm(string) for string in initialisation_sequence]
    return sum(vals)


def solve_part_2() -> int:
    initialisation_sequence = parse_input()
    boxes_map: defaultdict[int, dict] = defaultdict(dict)
    for string in initialisation_sequence:
        if string.endswith("-"):
            lens_label = string[:-1]
            box_number = run_hash_algorithm(lens_label)
            if lens_label in boxes_map[box_number]:
                del boxes_map[box_number][lens_label]
        elif "=" in string:
            lens_label, focal_length = string.split("=")
            box_number = run_hash_algorithm(lens_label)
            boxes_map[box_number][lens_label] = focal_length

        else:
            raise Exception(f"Invalid string: {string}. Should contain '=' or '-'")

    focussing_powers = [
        (box_number + 1) * i * int(v)
        for box_number, box_map in boxes_map.items()
        for i, v in enumerate(box_map.values(), 1)
    ]

    return sum(focussing_powers)


print(
    f"""
    Day 15: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
