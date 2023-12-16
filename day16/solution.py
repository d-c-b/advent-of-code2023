from os import path
from collections import deque
from typing import Iterator


def parse_input() -> list[list[str]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    return [[char for char in line] for line in lines]


BEAM_REFLECTION_SPLITTING_MAP = {
    "/": {(0, 1): [(-1, 0)], (1, 0): [(0, -1)], (0, -1): [(1, 0)], (-1, 0): [(0, 1)]},
    "\\": {(0, 1): [(1, 0)], (1, 0): [(0, 1)], (0, -1): [(-1, 0)], (-1, 0): [(0, -1)]},
    "|": {
        (0, 1): [(1, 0), (-1, 0)],
        (0, -1): [(1, 0), (-1, 0)],
        (1, 0): [(1, 0)],
        (-1, 0): [(-1, 0)],
    },
    "-": {
        (1, 0): [(0, 1), (0, -1)],
        (-1, 0): [(0, 1), (0, -1)],
        (0, 1): [(0, 1)],
        (0, -1): [(0, -1)],
    },
}


def solve(start_pos: tuple[int, int], start_dir: tuple[int, int]) -> int:
    grid = parse_input()
    energized_coords = set()

    beam_pos_dirs = deque([(start_pos, start_dir)])

    seen_position_direction_combinations = set()

    while beam_pos_dirs:
        beam_position, beam_direction = beam_pos_dirs.popleft()
        if (beam_position, beam_direction) in seen_position_direction_combinations:
            continue

        seen_position_direction_combinations.add((beam_position, beam_direction))
        current_y, current_x = beam_position
        dy, dx = beam_direction

        while 0 <= current_y < len(grid) and 0 <= current_x < len(grid[0]):
            energized_coords.add((current_y, current_x))
            if grid[current_y][current_x] == ".":
                current_y, current_x = (current_y + dy, current_x + dx)
            else:
                new_beam_pos_dirs = [
                    ((current_y + new_dy, current_x + new_dx), (new_dy, new_dx))
                    for (new_dy, new_dx) in BEAM_REFLECTION_SPLITTING_MAP[
                        grid[current_y][current_x]
                    ][beam_direction]
                ]
                beam_pos_dirs.extend(new_beam_pos_dirs)
                break

    return len(energized_coords)


def generate_edge_positions_and_directions(
    grid: list[list[str]],
) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    for x in range(len(grid[0])):
        yield ((0, x), (1, 0))
        yield ((len(grid) - 1, x), (-1, 0))

    for y in range(len(grid)):
        yield ((y, 0), (0, 1))
        yield ((y, len(grid[0]) - 1), (0, -1))


def solve_part_1() -> int:
    return solve((0, 0), (0, 1))


def solve_part_2() -> int:
    grid = parse_input()

    max_energised_tiles = 0

    for start_pos, start_dir in generate_edge_positions_and_directions(grid):
        energised_tiles = solve(start_pos, start_dir)
        max_energised_tiles = max(max_energised_tiles, energised_tiles)

    return max_energised_tiles


print(
    f"""
    Day 16: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
