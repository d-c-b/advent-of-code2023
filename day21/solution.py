from os import path
from collections import deque

DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))


def parse_input() -> tuple[tuple[int, int], set[tuple[int, int]], int]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    rock_positions = set()

    # check input is square
    assert len(lines[0]) == len(lines)
    grid_size = len(lines)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            if char == "#":
                rock_positions.add((x, y))

    return start, rock_positions, grid_size


def find_possible_end_positions(
    target_steps: int,
    start: tuple[int, int],
    rock_positions: set[tuple[int, int]],
    grid_size: int,
    infinite: bool = False,
) -> int:
    possible_positions = set()
    queue = deque([(0, start)])
    seen = set()
    while queue:
        steps, (x, y) = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))

        if steps % 2 == target_steps % 2:
            possible_positions.add((x, y))

        if steps < target_steps:
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (nx % grid_size, ny % grid_size) not in rock_positions:
                    if infinite or 0 <= nx < grid_size and 0 <= ny < grid_size:
                        queue.append((steps + 1, (nx, ny)))

    return len(possible_positions)


def solve_part_1() -> int:
    TARGET_STEPS = 64
    start, rock_positions, grid_size = parse_input()
    return find_possible_end_positions(TARGET_STEPS, start, rock_positions, grid_size)


def solve_part_2() -> int:
    TARGET_STEPS = 26501365
    start, rock_positions, grid_size = parse_input()
    distance_to_exit_plot_square = grid_size // 2  # starting point is in centre of grid

    step_targets = [distance_to_exit_plot_square + (i * grid_size) for i in range(3)]

    # find values for reachable squares for reaching edge of original grid
    # (x0), edge of first additional ring of copies of grid (x1) and edge of
    #  second additional ring of copies of grid (x2)
    x0, x1, x2 = [
        find_possible_end_positions(
            target_steps, start, rock_positions, grid_size, infinite=True
        )
        for target_steps in step_targets
    ]

    # This forms polynomial ax^2 + bx + c for x being number of rings of grid copies reached
    # find a, b and c for values of
    a = ((x2 - x0) // 2) - (x1 - x0)
    b = x1 - x0 - a
    c = x0

    # Find target x from number of steps (as this is takes to exactly
    # the edge of an integer number of grids rings)
    x_for_target = (TARGET_STEPS - distance_to_exit_plot_square) // grid_size

    return a * x_for_target**2 + b * x_for_target + c


print(
    f"""
    Day 21: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
