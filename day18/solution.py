from os import path


DIRECTIONS = {
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
    "U": (0, -1),
}

DIRECTION_NUMBER_TO_STRING = "RDLU"


def parse_input() -> list[tuple[str, int, str]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    direction_distance_hex = [line.split() for line in lines]
    return [
        (direction, int(distance), hex.strip("()#"))
        for (direction, distance, hex) in direction_distance_hex
    ]


def solve_part_1() -> int:
    instructions = parse_input()

    dug_positions = set([(0, 0)])
    current = (0, 0)
    for direction, distance, _ in instructions:
        for _ in range(distance):
            x, y = current
            new = (
                x + DIRECTIONS[direction][0],
                y + DIRECTIONS[direction][1],
            )
            dug_positions.add(new)
            current = new

    min_x, max_x = (
        min([x for x, _ in dug_positions]) - 1,
        max([x for x, _ in dug_positions]) + 1,
    )
    min_y, max_y = (
        min([y for _, y, in dug_positions]) - 1,
        max([y for _, y, in dug_positions]) + 1,
    )

    all_positions = set()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            all_positions.add((x, y))

    outside = set()
    to_visit = [(min_x, min_y)]

    while to_visit:
        current = to_visit.pop()
        outside.add(current)
        x, y = current
        neighbours = [(x + dx, y + dy) for dx, dy in DIRECTIONS.values()]
        for nx, ny in neighbours:
            if (
                (min_x <= nx <= max_x)
                and (min_y <= ny <= max_y)
                and ((nx, ny) not in dug_positions)
                and ((nx, ny) not in outside)
            ):
                to_visit.append((nx, ny))

    return len(all_positions - outside)


def solve_part_2() -> int:
    instructions = parse_input()
    dug_position_ranges: list[tuple[tuple[int, int], tuple[int, int]]] = []

    current = (0, 0)
    boundary_coord_count = 0
    for _, _, hex_code in instructions:
        distance = int(hex_code[:5], 16)
        direction = DIRECTION_NUMBER_TO_STRING[int(hex_code[5:], 16)]

        x, y = current
        current_range_end = (
            x + (distance * DIRECTIONS[direction][0]),
            y + (distance * DIRECTIONS[direction][1]),
        )

        dug_position_ranges.append((current, current_range_end))
        boundary_coord_count += distance

        current = current_range_end

    # Using Shoelace theorem to calculate total internal coordinates
    shoelace = 0
    for (x1, y1), (x2, y2) in dug_position_ranges:
        shoelace += x1 * y2 - x2 * y1
    internal_coords = shoelace // 2

    # Using Pick's theorem to calculate additional areaa for boundary
    area_from_boundary = boundary_coord_count // 2 + 1

    return internal_coords + area_from_boundary


print(
    f"""
    Day 18: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
