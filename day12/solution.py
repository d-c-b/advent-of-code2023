from os import path
import re
import itertools


def parse_input() -> list[tuple[str, tuple[int, ...]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    split_lines = [line.split() for line in input_file.read().strip().splitlines()]
    return [
        (spring_conditions, tuple([int(group) for group in damaged_groups.split(",")]))
        for spring_conditions, damaged_groups in split_lines
    ]


def solve_part_1() -> int:
    count = 0
    for spring_conditions, damaged_spring_group_sizes in parse_input():
        unknown_damaged_springs_count = sum(damaged_spring_group_sizes) - len(
            [spring for spring in spring_conditions if spring == "#"]
        )
        unknown_spring_indices = [
            i for i, char in enumerate(spring_conditions) if char == "?"
        ]

        for index_combination in itertools.combinations(
            unknown_spring_indices, unknown_damaged_springs_count
        ):
            spring_conditions_replaced = spring_conditions
            for index in index_combination:
                spring_conditions_replaced = (
                    spring_conditions_replaced[:index]
                    + "#"
                    + spring_conditions_replaced[index + 1 :]
                )

            spring_conditions_replaced = spring_conditions_replaced.replace("?", ".")
            if (
                tuple(
                    [
                        len(damaged_group)
                        for damaged_group in re.findall(
                            r"#+", spring_conditions_replaced
                        )
                    ]
                )
                == damaged_spring_group_sizes
            ):
                count += 1

    return count


class Solver:
    def __init__(self) -> None:
        self.MEMOISED_VALUES = dict()

    def number_of_valid_arrangements(
        self, string: str, groups: tuple[int, ...], active_group_length: int
    ) -> int:
        if (string, groups, active_group_length) in self.MEMOISED_VALUES:
            return self.MEMOISED_VALUES[(string, groups, active_group_length)]

        if len(groups) == 0:
            if all([char in ".?" for char in string]):
                return 1

            else:
                return 0

        if len(string) == 0:
            if len(groups) == 1 and active_group_length == groups[0]:
                return 1

            else:
                return 0

        valid_arrangements = 0
        if string[0] == ".":
            if active_group_length == 0:
                valid_arrangements += self.number_of_valid_arrangements(
                    string[1:], groups, 0
                )

            elif active_group_length > 0:
                if active_group_length == groups[0]:
                    valid_arrangements += self.number_of_valid_arrangements(
                        string[1:], groups[1:], 0
                    )
                else:
                    return 0

        elif string[0] == "#":
            if active_group_length < groups[0]:
                valid_arrangements += self.number_of_valid_arrangements(
                    string[1:], groups, active_group_length + 1
                )
            else:
                return 0

        elif string[0] == "?":
            if active_group_length == groups[0]:
                valid_arrangements += self.number_of_valid_arrangements(
                    string[1:], groups[1:], 0
                )

            if 0 < active_group_length < groups[0]:
                valid_arrangements += self.number_of_valid_arrangements(
                    string[1:], groups, active_group_length + 1
                )

            if active_group_length == 0:
                valid_arrangements += self.number_of_valid_arrangements(
                    string[1:], groups, 1
                ) + self.number_of_valid_arrangements(string[1:], groups, 0)

        self.MEMOISED_VALUES[(string, groups, active_group_length)] = valid_arrangements

        return valid_arrangements


def solve_part_2() -> int:
    spring_information = parse_input()
    count = 0
    for conditions, damaged_spring_group_sizes in spring_information:
        count += Solver().number_of_valid_arrangements(
            "?".join([conditions] * 5), damaged_spring_group_sizes * 5, 0
        )

    return count


print(
    f"""
    Day 12: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
