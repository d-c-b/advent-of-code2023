from os import path
import heapq


def parse_input() -> list[list[int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    return [[int(char) for char in line] for line in lines]


DIRECTIONS = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}


def solve_min_distance(
    grid: list[list[int]],
    start_position: tuple[int, int],
    end_position: tuple,
    max_steps_in_same_direction: int,
    min_steps_in_same_direction: int,
) -> int:
    SHORTEST_DISTANCES: dict[tuple[tuple[int, int], int, int], int] = dict()

    start = (0, start_position, 0, 0)
    queue = [start]

    while queue:
        key = heapq.heappop(queue)

        total_sum, (y, x), direction, steps_in_current_direction = key
        hash_vals = (y, x), direction, steps_in_current_direction
        if hash_vals in SHORTEST_DISTANCES:
            SHORTEST_DISTANCES[hash_vals] = min(
                total_sum,
                SHORTEST_DISTANCES[hash_vals],
            )
            continue

        SHORTEST_DISTANCES[(y, x), direction, steps_in_current_direction] = total_sum

        new_directions = [(direction + 1) % 4, (direction - 1) % 4, direction]

        for new_dir in new_directions:
            dy, dx = DIRECTIONS[new_dir]
            new_y, new_x = y + dy, x + dx
            if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]):
                if new_dir == direction:
                    new_k = (
                        total_sum + grid[new_y][new_x],
                        (new_y, new_x),
                        new_dir,
                        steps_in_current_direction + 1,
                    )
                    if steps_in_current_direction < max_steps_in_same_direction:
                        heapq.heappush(queue, new_k)

                else:
                    if steps_in_current_direction >= min_steps_in_same_direction:
                        new_k = (
                            total_sum + grid[new_y][new_x],
                            (new_y, new_x),
                            new_dir,
                            1,
                        )
                        heapq.heappush(queue, new_k)

    return min([v for k, v in SHORTEST_DISTANCES.items() if k[0] == end_position])


def solve_part_1() -> int:
    grid = parse_input()
    return solve_min_distance(
        grid,
        (0, 0),
        (len(grid) - 1, len(grid[0]) - 1),
        max_steps_in_same_direction=3,
        min_steps_in_same_direction=1,
    )


def solve_part_2() -> int:
    grid = parse_input()
    return solve_min_distance(
        grid,
        (0, 0),
        (len(grid) - 1, len(grid[0]) - 1),
        max_steps_in_same_direction=10,
        min_steps_in_same_direction=4,
    )


print(
    f"""
    Day 17: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
