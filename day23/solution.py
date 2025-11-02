from os import path
from collections import deque, defaultdict


DIRECTIONS_MAP = {
    ".": [(0, 1), (1, 0), (-1, 0), (0, -1)],
    ">": [(1, 0)],
    "v": [(0, 1)],
}


def parse_input() -> (
    tuple[dict[tuple[int, int], str], tuple[int, int], tuple[int, int]]
):
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    path_map = dict()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != "#":
                path_map[(x, y)] = char
            if y == 0 and char == ".":
                start = (x, y)

            if y == len(lines) - 1 and char == ".":
                end = (x, y)
    return path_map, start, end


class TrailMap:
    def __init__(
        self,
        path_map: dict[tuple[int, int], str],
        start: tuple[int, int],
        end: tuple[int, int],
        ignore_slopes: bool = False,
    ) -> None:
        self.start = start
        self.end = end
        self.path_map = path_map
        self.ignore_slopes = ignore_slopes
        self.graph: defaultdict[tuple[int, int], list] = defaultdict(list)

        for node in self.path_map:
            self.graph[node].extend(
                [(neighbour, 1) for neighbour in self.neighbouring_spaces(node)]
            )

    def neighbouring_spaces(self, coords: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = coords
        DIRECTIONS = (
            DIRECTIONS_MAP["."]
            if self.ignore_slopes
            else DIRECTIONS_MAP[self.path_map[(x, y)]]
        )
        neighbours = [(x + dx, y + dy) for dx, dy in DIRECTIONS]
        allowed = [neighbour for neighbour in neighbours if neighbour in self.path_map]

        return allowed

    def condense_graph(self) -> None:
        nodes: defaultdict[tuple[int, int], list] = defaultdict(list)
        queue = deque([(0, self.start, [self.start])])
        seen = set()
        while queue:
            path_length, (x, y), path_taken = queue.pop()
            possible_neighbours = self.neighbouring_spaces((x, y))
            reachable = [
                neighbour
                for neighbour in possible_neighbours
                if neighbour not in path_taken
            ]

            if len(reachable) == 1:
                queue.append((path_length + 1, reachable[0], [*path_taken, (x, y)]))

            elif len(reachable) > 1:
                start_node, *_ = path_taken
                if tuple(sorted((start_node, (x, y)))) in seen:
                    continue
                nodes[start_node].append(((x, y), path_length))
                nodes[(x, y)].append((start_node, path_length))
                seen.add(tuple(sorted((start_node, (x, y)))))
                for r in reachable:
                    queue.append((1, r, [(x, y), r]))

            else:
                if (x, y) == self.end:
                    start_node, *_ = path_taken
                    nodes[start_node].append(((x, y), path_length))
                    nodes[(x, y)].append((start_node, path_length))

        self.condensed_graph = nodes

    def find_longest_path(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        use_condensed_graph: bool = False,
    ):
        graph = self.condensed_graph if use_condensed_graph else self.graph
        queue = deque([(0, start, [start])])
        longest = 0
        while queue:
            path_length, (x, y), path_taken = queue.pop()

            if (x, y) == end:
                longest = max(path_length, longest)
                continue

            for neighbour, distance in graph[(x, y)]:
                if neighbour not in path_taken:
                    queue.append(
                        (path_length + distance, neighbour, [*path_taken, (x, y)])
                    )

        return longest


def solve_part_1() -> int:
    path_map, start, end = parse_input()
    trail_map = TrailMap(path_map=path_map, start=start, end=end)
    return trail_map.find_longest_path(start, end)


def solve_part_2() -> int:
    path_map, start, end = parse_input()
    trail_map = TrailMap(path_map=path_map, start=start, end=end, ignore_slopes=True)
    trail_map.condense_graph()
    return trail_map.find_longest_path(start, end, use_condensed_graph=True)


print(
    f"""
    Day 23: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
