from os import path

DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))

CONNECTION_MAP = {
    (0, 1): {"|": (0, 1), "L": (1, 0), "J": (-1, 0)},
    (0, -1): {"|": (0, -1), "F": (1, 0), "7": (-1, 0)},
    (1, 0): {"-": (1, 0), "J": (0, -1), "7": (0, 1)},
    (-1, 0): {"-": (-1, 0), "L": (0, -1), "F": (0, 1)},
}


def parse_input() -> tuple[dict[tuple[int, int], str], tuple[int, int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    grid_input = dict()
    start_position = (0, 0)
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char != ".":
                grid_input[(i, j)] = char

            if char == "S":
                start_position = (i, j)
    return grid_input, start_position


class PipeCoordinateGrid:
    def __init__(
        self, grid_input: dict[tuple[int, int], str], start_position: tuple[int, int]
    ):
        self.grid = grid_input
        self.start_position = start_position
        self.loop_coordinates_set = self.find_loop_coordinate_set()
        self.min_x, self.max_x = (
            min([x for x, _ in self.loop_coordinates_set]) - 1,
            max([x for x, _ in self.loop_coordinates_set]) + 1,
        )
        self.min_y, self.max_y = (
            min([y for _, y in self.loop_coordinates_set]) - 1,
            max([y for _, y in self.loop_coordinates_set]) + 1,
        )

    def take_step(
        self,
        position: tuple[int, int],
        direction: tuple[int, int] | None,
    ) -> tuple[tuple[int, int], tuple[int, int] | None]:
        if not direction:
            raise Exception(
                f"No direction provided when trying to take step at position: {position}"
            )
        new_position = (position[0] + direction[0], position[1] + direction[1])
        new_direction = CONNECTION_MAP[direction].get(self.grid[new_position])
        return new_position, new_direction

    def find_loop_coordinate_set(self) -> set[tuple[int, int]]:
        x, y = self.start_position
        possible_start_directions = [
            (dx, dy)
            for dx, dy in DIRECTIONS
            if (x + dx, y + dy) in self.grid
            and self.take_step(self.start_position, (dx, dy))
        ]
        for possible_start_direction in possible_start_directions:
            current_pos, current_dir = self.take_step(
                self.start_position, possible_start_direction
            )
            valid_loop = True
            loop_coords = set([self.start_position, current_pos])
            while current_pos != self.start_position:
                new_pos, new_dir = self.take_step(current_pos, current_dir)
                if not new_dir and self.grid[new_pos] != "S":
                    valid_loop = False
                    break
                current_pos, current_dir = new_pos, new_dir
                loop_coords.add(current_pos)
            if valid_loop:
                return loop_coords
        raise Exception(
            f"No valid loop found from starting position {self.start_position}"
        )

    def flood_fill_around_loop_coordinates(self) -> set[tuple[int, int]]:
        outside_coords = set()
        to_visit = [(self.min_x, self.min_y)]
        while to_visit:
            x, y = to_visit.pop()
            if (x, y) in outside_coords:
                continue
            outside_coords.add((x, y))
            neighbouring_coords = [
                (x + dx, y + dy)
                for dx, dy in DIRECTIONS
                if (self.min_x <= x + dx <= self.max_x)
                and (self.min_y <= y + dy <= self.max_y)
            ]
            for neighbour in neighbouring_coords:
                if neighbour not in self.loop_coordinates_set:
                    to_visit.append(neighbour)

        return outside_coords

    def find_loop_enclosed_coordinate_set(self) -> set[tuple[int, int]]:
        outside_loop_coords = self.flood_fill_around_loop_coordinates()
        all_points_within_range = set(
            (x, y)
            for x in range(self.min_x, self.max_x + 1)
            for y in range(self.min_y, self.max_y + 1)
        )
        points_within_loop = (
            all_points_within_range - outside_loop_coords - self.loop_coordinates_set
        )

        non_enclosed_within_loop = set()
        for point in points_within_loop:
            curr = point
            loop_intersections_count = 0
            while curr not in outside_loop_coords:
                curr_x, curr_y = curr
                curr = (curr_x - 1, curr_y)
                if (
                    curr in self.grid
                    and curr in self.loop_coordinates_set
                    and self.grid[curr] in "LJ|"
                ):
                    loop_intersections_count += 1

            if loop_intersections_count % 2 == 0:
                non_enclosed_within_loop.add(point)

        return (
            all_points_within_range
            - outside_loop_coords
            - self.loop_coordinates_set
            - non_enclosed_within_loop
        )


def solve_part_1() -> int:
    grid_input, start_position = parse_input()
    grid = PipeCoordinateGrid(grid_input, start_position)
    return len(grid.loop_coordinates_set) // 2


def solve_part_2() -> int:
    grid_input, start_position = parse_input()
    grid = PipeCoordinateGrid(grid_input, start_position)
    enclosed_coordinates = grid.find_loop_enclosed_coordinate_set()
    return len(enclosed_coordinates)


print(
    f"""
    Day 10: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
