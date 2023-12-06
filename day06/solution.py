from os import path
import math
from typing import Iterator


def parse_input() -> tuple[Iterator[tuple[int, int]], tuple[int, int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    time_input, distance_input = input_file.read().strip().splitlines()

    time_values_separated = [int(x) for x in time_input.split()[1:]]
    distance_values_separated = [int(x) for x in distance_input.split()[1:]]

    time_value_joined = int("".join(str(t) for t in time_values_separated))
    record_distance_joined = int("".join([str(d) for d in distance_values_separated]))

    return zip(time_values_separated, distance_values_separated), (
        time_value_joined,
        record_distance_joined,
    )


def calculate_distance(t: int, total_time: int) -> int:
    return t * (total_time - t)


def solve_part_1() -> int:
    races, _ = parse_input()
    winning_strategies_counts = []
    for time, record_distance in races:
        winning_strategies = 0
        for hold_time in range(time):
            distance = calculate_distance(hold_time, time)
            if distance > record_distance:
                winning_strategies += 1

        winning_strategies_counts.append(winning_strategies)

    return math.prod(winning_strategies_counts)


def midpoint(start: int, end: int) -> int:
    return start + ((end - start) // 2)


def solve_part_2() -> int:
    _, (time, record_distance) = parse_input()

    lower_bound_start, upper_bound_start = 0, time
    while calculate_distance(lower_bound_start, time) < record_distance:
        mid_point = midpoint(lower_bound_start, upper_bound_start)
        if mid_point == lower_bound_start:
            break

        if calculate_distance(mid_point, time) > record_distance:
            upper_bound_start = mid_point

        else:
            lower_bound_start = mid_point
        first_winning_time = lower_bound_start + 1

    lower_bound_end, upper_bound_end = lower_bound_start + 1, time
    while calculate_distance(lower_bound_end, time) > record_distance:
        mid_point = midpoint(lower_bound_end, upper_bound_end)
        if mid_point == lower_bound_end:
            break

        if calculate_distance(mid_point, time) > record_distance:
            lower_bound_end = mid_point

        else:
            upper_bound_end = mid_point
        last_winning_time = lower_bound_end

    return last_winning_time - first_winning_time + 1


print(
    f"""
    Day 06: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
