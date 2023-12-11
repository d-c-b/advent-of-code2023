from os import path
import itertools


def parse_input() -> set[tuple[int, int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    galaxy_coordinates = set()
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == "#":
                galaxy_coordinates.add((i, j))
    return galaxy_coordinates


def find_empty_row_column_coords(
    galaxy_coordinates: set[tuple[int, int]]
) -> tuple[set[int], set[int]]:
    all_x_coords = [x for (x, _) in galaxy_coordinates]
    min_x, max_x = min(all_x_coords), max(all_x_coords)

    all_y_coords = [y for (_, y) in galaxy_coordinates]
    min_y, max_y = min(all_y_coords), max(all_y_coords)
    empty_column_x_coords = set()
    empty_row_y_coords = set()

    for i in range(min_x, max_x):
        if all([i != x for (x, _) in galaxy_coordinates]):
            empty_column_x_coords.add(i)

    for j in range(min_y, max_y):
        if all([j != y for (_, y) in galaxy_coordinates]):
            empty_row_y_coords.add(j)

    return empty_row_y_coords, empty_column_x_coords


def solve(galaxy_coordinates: set[tuple[int, int]], expansion_factor: int) -> int:
    empty_row_y_coords, empty_column_x_coords = find_empty_row_column_coords(
        galaxy_coordinates
    )

    distance_sum = 0
    for (g1x, g1y), (g2x, g2y) in itertools.combinations(galaxy_coordinates, 2):
        number_of_empty_columns_between = len(
            [
                x
                for x in range(min(g1x, g2x), max(g1x, g2x))
                if x in empty_column_x_coords
            ]
        )
        number_of_empty_rows_between = len(
            [y for y in range(min(g1y, g2y), max(g1y, g2y)) if y in empty_row_y_coords]
        )

        distance = (
            abs(g1x - g2x)
            + abs(g1y - g2y)
            + (
                (number_of_empty_columns_between + number_of_empty_rows_between)
                * (expansion_factor - 1)
            )
        )
        distance_sum += distance

    return distance_sum


def solve_part_1() -> int:
    galaxy_coordinates = parse_input()
    return solve(galaxy_coordinates, 2)


def solve_part_2() -> int:
    galaxy_coordinates = parse_input()
    return solve(galaxy_coordinates, 1_000_000)


print(
    f"""
    Day 11: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
