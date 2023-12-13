from os import path
from collections import defaultdict


def parse_input() -> list[list[list[str]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    squares = input_file.read().strip().split("\n\n")
    return [[[c for c in line] for line in square.split("\n")] for square in squares]


def symmetry_differences(pair: tuple[int, int], line: list[str]) -> int:
    i, j = pair
    differences = 0
    while i >= 0 and j < len(line):
        if line[i] != line[j]:
            differences += 1

        i, j = i - 1, j + 1

    return differences


def sum_line_of_symmetry_for_square(
    square: list[list[str]], number_of_differences: int = 0
):
    pairs = list(zip(range(len(square[0])), range(1, len(square[0]))))

    diffs_for_pairs: defaultdict[tuple[int, int], int] = defaultdict(int)

    for line in square:
        for pair in pairs:
            diffs_for_pairs[pair] += symmetry_differences(pair, line)

    possible_pairs = [
        k for k, v in diffs_for_pairs.items() if v == number_of_differences
    ]
    return sum([smaller + 1 for smaller, _ in possible_pairs])


def solve_part_1() -> int:
    squares = parse_input()
    summarized = 0
    for square in squares:
        summarized += sum_line_of_symmetry_for_square(square)
        summarized += 100 * sum_line_of_symmetry_for_square(
            [[r[index] for r in square] for index in range(len(square[0]))]
        )

    return summarized


def solve_part_2() -> int:
    squares = parse_input()

    summarized = 0
    for square in squares:
        summarized += sum_line_of_symmetry_for_square(square, 1)
        summarized += 100 * sum_line_of_symmetry_for_square(
            [[r[index] for r in square] for index in range(len(square[0]))], 1
        )

    return summarized


print(
    f"""
    Day 13: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
