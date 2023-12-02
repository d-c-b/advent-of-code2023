from os import path
import re
from collections import defaultdict
import math

CUBE_COLOURS = ["red", "green", "blue"]

MAX_COLOURS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_input() -> dict[int, list[defaultdict[str, int]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    game_inputs = input_file.read().strip().splitlines()
    input_dict = {}
    for game in game_inputs:
        game_number, round_results = game.split(":")
        if not re.match(r"Game \d+$", game_number):
            raise Exception(
                f"Invalid input line - cannot determine game number: {game_number}"
            )

        game_id = int(game_number.split(" ")[1])
        rounds = [
            round_result.strip().split(", ")
            for round_result in round_results.split(";")
        ]

        round_results_list = []
        for round in rounds:
            round_dict: defaultdict[str, int] = defaultdict(int)
            for cube_input in round:
                if not re.match(rf"\d+ ({'|'.join(CUBE_COLOURS)})$", cube_input):
                    raise Exception(f"Invalid input for round in: {game}")
                for colour in CUBE_COLOURS:
                    if colour in cube_input:
                        round_dict[colour] += int(cube_input.split()[0])

            round_results_list.append(round_dict)

        input_dict[game_id] = round_results_list

    return input_dict


def solve_part_1() -> int:
    input_dict = parse_input()
    possible_ids_sum = 0
    for game_id, rounds in input_dict.items():
        if all(
            [
                all([r[colour] <= MAX_COLOURS[colour] for colour in CUBE_COLOURS])
                for r in rounds
            ]
        ):
            possible_ids_sum += game_id
    return possible_ids_sum


def solve_part_2() -> int:
    input_dict = parse_input()
    minimum_powers_sum = 0
    for rounds in input_dict.values():
        minimums: defaultdict[str, int] = defaultdict(int)
        for round in rounds:
            for colour in CUBE_COLOURS:
                minimums[colour] = max(minimums[colour], round[colour])

        minimum_power = math.prod(minimums.values())
        minimum_powers_sum += minimum_power

    return minimum_powers_sum


print(
    f"""
    Day 02: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
