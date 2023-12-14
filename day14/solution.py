from os import path
import itertools


class RockGrid:
    def __init__(
        self,
        round_rocks: set[tuple[int, int]],
        square_rocks: set[tuple[int, int]],
        MAX_X: int,
        MAX_Y: int,
    ) -> None:
        self.SEEN_STATES: dict[frozenset[tuple[int, int]], int] = dict()
        self.round_rocks = round_rocks
        self.square_rocks = square_rocks
        self.MAX_X = MAX_X
        self.MAX_Y = MAX_Y

    def calculate_load_on_north(
        self, round_rocks: set[tuple[int, int]] | frozenset[tuple[int, int]]
    ) -> int:
        load = 0
        for a, b in zip(range(self.MAX_Y), range(self.MAX_Y - 1, -1, -1)):
            load += len([(x, y) for (x, y) in round_rocks if y == b]) * (a + 1)

        return load

    def roll_rocks_north(self):
        for j in range(0, self.MAX_Y + 1):
            for x, y in [(x, y) for (x, y) in self.round_rocks if y == j]:
                current = y
                while (
                    current - 1 >= 0
                    and (x, current - 1) not in self.round_rocks | self.square_rocks
                ):
                    self.round_rocks.remove((x, current))
                    self.round_rocks.add((x, current - 1))

                    current -= 1

    def roll_rocks_south(self):
        for j in range(self.MAX_Y, -1, -1):
            for x, y in [(x, y) for (x, y) in self.round_rocks if y == j]:
                current = y
                while (
                    current + 1 <= self.MAX_Y - 1
                    and (x, current + 1) not in self.round_rocks | self.square_rocks
                ):
                    self.round_rocks.remove((x, current))
                    self.round_rocks.add((x, current + 1))

                    current += 1

    def roll_rocks_east(self):
        for i in range(self.MAX_X, -1, -1):
            for x, y in [(x, y) for (x, y) in self.round_rocks if x == i]:
                current = x
                while (
                    current + 1 <= self.MAX_X - 1
                    and (current + 1, y) not in self.round_rocks | self.square_rocks
                ):
                    self.round_rocks.remove((current, y))
                    self.round_rocks.add((current + 1, y))
                    current += 1

    def roll_rocks_west(self):
        for i in range(0, self.MAX_X + 1):
            for x, y in [(x, y) for (x, y) in self.round_rocks if x == i]:
                current = x
                while (
                    current - 1 >= 0
                    and (current - 1, y) not in self.round_rocks | self.square_rocks
                ):
                    self.round_rocks.remove((current, y))
                    self.round_rocks.add((current - 1, y))

                    current -= 1

    def detect_repeating_cycle_in_rolling(self) -> tuple[int, int]:
        for i in itertools.count():
            if frozenset(self.round_rocks) in self.SEEN_STATES:
                first_seen_iteration = self.SEEN_STATES[frozenset(self.round_rocks)]
                cycle_repeat_length = i - first_seen_iteration

                return first_seen_iteration, cycle_repeat_length

            else:
                self.SEEN_STATES[frozenset(self.round_rocks)] = i

            self.roll_rocks_north()
            self.roll_rocks_west()
            self.roll_rocks_south()
            self.roll_rocks_east()

        raise Exception("Failed to find cycle pattern in data")


def parse_input() -> tuple[set[tuple[int, int]], set[tuple[int, int]], int, int]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    round_rocks = set()
    square_rocks = set()
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == "O":
                round_rocks.add((i, j))
            if char == "#":
                square_rocks.add((i, j))

    MAX_Y = len(lines)
    MAX_X = len(lines[0])
    return round_rocks, square_rocks, MAX_Y, MAX_X


def solve_part_1() -> int:
    round_rocks, square_rocks, MAX_Y, MAX_X = parse_input()
    rock_grid = RockGrid(round_rocks, square_rocks, MAX_Y, MAX_X)
    rock_grid.roll_rocks_north()
    return rock_grid.calculate_load_on_north(rock_grid.round_rocks)


def solve_part_2() -> int:
    round_rocks, square_rocks, MAX_Y, MAX_X = parse_input()
    rock_grid = RockGrid(round_rocks, square_rocks, MAX_Y, MAX_X)

    (
        first_seen_iteration,
        cycle_repeat_length,
    ) = rock_grid.detect_repeating_cycle_in_rolling()

    seen_id_billionth = (
        first_seen_iteration
        + (1_000_000_000 - first_seen_iteration) % cycle_repeat_length
    )

    billionth_iteration = list(rock_grid.SEEN_STATES.keys())[
        list(rock_grid.SEEN_STATES.values()).index(seen_id_billionth)
    ]
    return rock_grid.calculate_load_on_north(billionth_iteration)


print(
    f"""
    Day 14: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
