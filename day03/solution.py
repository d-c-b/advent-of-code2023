from os import path
import math

ADJACENT_COORDS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def parse_input() -> tuple[dict[tuple[int, int], str], int, int]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    input_lines = input_file.read().strip().splitlines()
    grid = {}
    for j, line in enumerate(input_lines):
        for i, char in enumerate(line):
            grid[(i, j)] = char

    X_MAX = len(input_lines[0])
    Y_MAX = len(input_lines)
    return grid, X_MAX, Y_MAX


def find_coords_of_full_number(
    coords: tuple[int, int], schematic: dict[tuple[int, int], str]
) -> tuple[tuple[int, int], ...]:
    x, y = coords
    min_x, max_x = x, x

    while schematic.get((min_x, y)) and schematic[(min_x, y)].isdigit():
        min_x -= 1

    while schematic.get((max_x, y)) and schematic[(max_x, y)].isdigit():
        max_x += 1

    return tuple([(x, y) for x in range(min_x + 1, max_x)])


def solve_part_1() -> int:
    schematic, X_MAX, Y_MAX = parse_input()

    number_coords_set = set()
    for y in range(Y_MAX):
        for x in range(X_MAX):
            if schematic[(x, y)].isdigit():
                number_coords_set.add(find_coords_of_full_number((x, y), schematic))

    part_number_sum = 0
    for number_coords in number_coords_set:
        adjacent_chars = [
            schematic.get((nx + dx, ny + dy))
            for dx, dy in ADJACENT_COORDS
            for nx, ny in number_coords
        ]
        adjacent_symbols = [
            x for x in adjacent_chars if x and not x.isdigit() and x != "."
        ]
        if any(adjacent_symbols):
            part_number_sum += int(
                "".join([schematic[(i, j)] for i, j in number_coords])
            )
    return part_number_sum


def solve_part_2() -> int:
    schematic, X_MAX, Y_MAX = parse_input()
    asterisk_positions = [
        (x, y) for x in range(X_MAX) for y in range(Y_MAX) if schematic[(x, y)] == "*"
    ]

    sum_of_gear_ratios = 0
    for asterisk_coord in asterisk_positions:
        ast_x, ast_y = asterisk_coord
        adjacent_coords = [(ast_x + dx, ast_y + dy) for dx, dy in ADJACENT_COORDS]
        coords_of_adjacent_numbers = set(
            [
                find_coords_of_full_number((x, y), schematic)
                for x, y in adjacent_coords
                if schematic.get((x, y)) and schematic[(x, y)].isdigit()
            ]
        )
        if len(coords_of_adjacent_numbers) == 2:
            adjacent_numbers = [
                int("".join([schematic[(x, y)] for x, y in coord]))
                for coord in coords_of_adjacent_numbers
            ]
            sum_of_gear_ratios += math.prod(adjacent_numbers)

    return sum_of_gear_ratios


print(
    f"""
    Day 03: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
