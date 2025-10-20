from os import path
from collections import defaultdict, deque
from typing import cast


def parse_input() -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()

    bricks = list()
    for line in lines:
        start_pos, end_pos = line.split("~")
        start = cast(
            tuple[int, int, int], tuple([int(coord) for coord in start_pos.split(",")])
        )
        end = cast(
            tuple[int, int, int], tuple(int(coord) for coord in end_pos.split(","))
        )
        bricks.append((start, end))

    return bricks


class Stack:
    def __init__(
        self, bricks: list[tuple[tuple[int, int, int], tuple[int, int, int]]]
    ) -> None:
        self.bricks_to_drop = sorted(
            bricks, key=lambda brick: min(brick[0][2], brick[1][2])
        )
        self.max_heights: defaultdict[
            tuple[int, int], tuple[int, int | None]
        ] = defaultdict(lambda: (0, None))
        self.supported_by: dict[int, set[int]] = dict()
        self.is_supporting: defaultdict[int, set[int]] = defaultdict(set)

    def drop_bricks(self) -> None:
        for brick_id, brick in enumerate(self.bricks_to_drop):
            (x1, y1, z1), (x2, y2, z2) = brick
            min_z = min(z1, z2)
            filled_positions = set(
                [
                    (x, y, z)
                    for z in range(z1, z2 + 1)
                    for y in range(y1, y2 + 1)
                    for x in range(x1, x2 + 1)
                ]
            )

            bottom_surface_x_y = set(
                [(x, y) for (x, y, z) in filled_positions if z == min_z]
            )
            dist_to_drop = min(
                [min_z - self.max_heights[x_y][0] - 1 for x_y in bottom_surface_x_y]
            )
            settled_positions = set(
                [(x, y, z - dist_to_drop) for (x, y, z) in filled_positions]
            )

            support_bricks = set(
                [
                    support_brick
                    for _, support_brick in [
                        self.max_heights[((x, y))]
                        for (x, y, z) in settled_positions
                        if self.max_heights[((x, y))][0] == z - 1
                    ]
                    if support_brick is not None
                ]
            )

            self.supported_by[brick_id] = support_bricks
            for support_brick in support_bricks:
                self.is_supporting[support_brick].add(brick_id)

            for x, y, z in settled_positions:
                self.max_heights[(x, y)] = (
                    max(z, self.max_heights[(x, y)][0]),
                    brick_id,
                )


def solve_part_1() -> int:
    bricks = parse_input()
    stack = Stack(bricks)
    stack.drop_bricks()

    cannot_disintegrate = set()
    for supporting_bricks in stack.supported_by.values():
        if len(supporting_bricks) == 1:
            cannot_disintegrate.update(supporting_bricks)

    return len(stack.bricks_to_drop) - len(cannot_disintegrate)


def solve_part_2() -> int:
    bricks = parse_input()
    stack = Stack(bricks)
    stack.drop_bricks()

    total_falling = 0
    for brick_id, bricks_supported in stack.is_supporting.items():
        falling: set[int] = set()
        to_check = deque(
            [(brick_id, brick_supported) for brick_supported in bricks_supported]
        )

        while to_check:
            supporting, supported = to_check.popleft()
            if not stack.supported_by[supported] - set([supporting]) - falling:
                falling.add(supported)
                if supported in stack.is_supporting:
                    to_check.extend(
                        [(supported, brick) for brick in stack.is_supporting[supported]]
                    )
        total_falling += len(falling)
    return total_falling


print(
    f"""
    Day 22: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
