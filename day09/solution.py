from os import path


def parse_input() -> list[list[int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    return [[int(val) for val in line.split()] for line in lines]


def get_list_of_differential_series(sequence: list[int]) -> list[list[int]]:
    diffs_list = [sequence]
    current = sequence
    while not all([diff == 0 for diff in current]):
        current = [current[i + 1] - current[i] for i in range(len(current) - 1)]
        diffs_list.append(current)
    return diffs_list


def solve_for_next_in_sequence(sequence: list[int]) -> int:
    diffs_list = get_list_of_differential_series(sequence)
    next_in_sequence = diffs_list[-1][-1]
    for differential_order in range(len(diffs_list) - 1, -1, -1):
        next_in_sequence += diffs_list[differential_order][-1]
    return next_in_sequence


def solve_part_1() -> int:
    values_lists = parse_input()
    next_values_for_sequences = []
    for sequence in values_lists:
        next_in_sequence = solve_for_next_in_sequence(sequence)
        next_values_for_sequences.append(next_in_sequence)
    return sum(next_values_for_sequences)


def solve_part_2() -> int:
    values_lists = parse_input()
    next_values_for_sequences = []
    for sequence in values_lists:
        next_in_sequence = solve_for_next_in_sequence(sequence[::-1])
        next_values_for_sequences.append(next_in_sequence)
    return sum(next_values_for_sequences)


print(
    f"""
    Day 09: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
