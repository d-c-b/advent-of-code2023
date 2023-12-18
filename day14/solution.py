from os import path
import itertools


class RockGrid:
    def __init__(
        self,
        grid: list[list[str]],
    ) -> None:
        self.SEEN_STATES: dict[tuple[tuple[str, ...], ...], int] = dict()
        self.grid = grid
        self.MAX_X = len(grid[0])
        self.MAX_Y = len(grid)

    def calculate_load_on_north(
        self, grid: list[list[str]] | tuple[tuple[str, ...], ...]
    ) -> int:
        load = 0
        for y in range(self.MAX_Y):
            for x in range(self.MAX_X):
                if grid[y][x] == "O":
                    load += self.MAX_Y - y
        return load

    def roll_rocks_north(self):
        for y in range(0, self.MAX_Y):
            for x in range(0, self.MAX_X):
                current = y
                while (
                    current - 1 >= 0
                    and self.grid[current][x] == "O"
                    and self.grid[current - 1][x] not in "#O"
                ):
                    self.grid[current][x] = "."
                    self.grid[current - 1][x] = "O"
                    current -= 1

    def roll_rocks_south(self):
        for y in range(self.MAX_Y - 1, -1, -1):
            for x in range(0, self.MAX_X):
                current = y
                while (
                    current + 1 < self.MAX_Y
                    and self.grid[current][x] == "O"
                    and self.grid[current + 1][x] not in "#O"
                ):
                    self.grid[current][x] = "."
                    self.grid[current + 1][x] = "O"
                    current += 1

    def roll_rocks_east(self):
        for x in range(self.MAX_X - 1, -1, -1):
            for y in range(0, self.MAX_Y):
                current = x
                while (
                    current + 1 < self.MAX_X
                    and self.grid[y][current] == "O"
                    and self.grid[y][current + 1] not in "#O"
                ):
                    self.grid[y][current] = "."
                    self.grid[y][current + 1] = "O"
                    current += 1

    def roll_rocks_west(self):
        for x in range(0, self.MAX_X):
            for y in range(0, self.MAX_Y):
                current = x
                while (
                    current - 1 >= 0
                    and self.grid[y][current] == "O"
                    and self.grid[y][current - 1] not in "#O"
                ):
                    self.grid[y][current] = "."
                    self.grid[y][current - 1] = "O"
                    current -= 1

    def detect_repeating_cycle_in_rolling(self) -> tuple[int, int]:
        for i in itertools.count():
            hashable_grid = tuple(tuple(row) for row in self.grid)
            if hashable_grid in self.SEEN_STATES:
                first_seen_iteration = self.SEEN_STATES[hashable_grid]
                cycle_repeat_length = i - first_seen_iteration

                return first_seen_iteration, cycle_repeat_length

            else:
                self.SEEN_STATES[hashable_grid] = i

            self.roll_rocks_north()
            self.roll_rocks_west()
            self.roll_rocks_south()
            self.roll_rocks_east()

        raise Exception("Failed to find cycle pattern in data")


def parse_input() -> list[list[str]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    return [[char for char in line] for line in lines]


def solve_part_1() -> int:
    grid = parse_input()
    rock_grid = RockGrid(grid)
    rock_grid.roll_rocks_north()
    return rock_grid.calculate_load_on_north(rock_grid.grid)


def solve_part_2() -> int:
    grid = parse_input()
    rock_grid = RockGrid(grid)

    (
        first_seen_iteration,
        cycle_repeat_length,
    ) = rock_grid.detect_repeating_cycle_in_rolling()

    first_seen_iteration_number_of_billionth = (
        first_seen_iteration
        + (1_000_000_000 - first_seen_iteration) % cycle_repeat_length
    )

    billionth_iteration = list(rock_grid.SEEN_STATES.keys())[
        list(rock_grid.SEEN_STATES.values()).index(
            first_seen_iteration_number_of_billionth
        )
    ]
    return rock_grid.calculate_load_on_north(billionth_iteration)


print(
    f"""
    Day 14: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
