from __future__ import annotations
from os import path


def parse_input() -> tuple[list[int], list[list[list[int]]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    input_groups = input_file.read().strip().split("\n\n")
    seed_numbers = [int(seed) for seed in input_groups[0].split(": ")[1].split()]
    seed_mappings = []
    for mapping in [line.splitlines()[1:] for line in input_groups[1:]]:
        mapping_ranges = [[int(x) for x in s.split()] for s in mapping]
        seed_mappings.append(mapping_ranges)
    return seed_numbers, seed_mappings


def find_in_ranges(num: int, ranges: list[list[int]]) -> int:
    for destination_start, source_start, range_size in ranges:
        if num >= source_start and num < source_start + range_size:
            return destination_start + num - source_start
    return num


def solve_part_1() -> int:
    seed_numbers, seed_mappings = parse_input()
    location_numbers = []
    for seed in seed_numbers:
        prev = seed
        for mapping in seed_mappings:
            prev = find_in_ranges(prev, mapping)
        location_numbers.append(prev)
    return min(location_numbers)


class Range:
    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.length = length
        self.end = start + length

    def overlapping_range(self, other_range: Range) -> Range | None:
        max_start = max(self.start, other_range.start)
        min_end = min(self.end, other_range.end)

        if max_start < min_end:
            return Range(max_start, min_end - max_start)

        return None

    def remove_range(self, range_to_remove) -> list[Range]:
        remaining_ranges_after_removal = []
        if self.start < range_to_remove.start:
            remaining_ranges_after_removal.append(
                Range(self.start, range_to_remove.start - self.start)
            )

        if self.end > range_to_remove.end:
            remaining_ranges_after_removal.append(
                Range(
                    max(range_to_remove.end, self.start), self.end - range_to_remove.end
                )
            )
        return remaining_ranges_after_removal


def apply_mapping_range(
    mapping_range: Range, mapping_destination_start: int, seed_range: Range
) -> tuple[list[Range], list[Range]]:
    mapped_ranges = []
    overlapping_section = mapping_range.overlapping_range(seed_range)
    if overlapping_section:
        mapped_overlapping = Range(
            overlapping_section.start - mapping_range.start + mapping_destination_start,
            overlapping_section.length,
        )
        mapped_ranges.append(mapped_overlapping)
        non_mapped_ranges = seed_range.remove_range(overlapping_section)

    else:
        non_mapped_ranges = [seed_range]

    return mapped_ranges, non_mapped_ranges


def solve_part_2() -> int:
    seed_numbers, seed_maps = parse_input()
    seed_numbers_ranges = [
        Range(seed_numbers[i], seed_numbers[i + 1])
        for i in range(0, len(seed_numbers), 2)
    ]
    seed_mappings = [
        [
            (destination_start, Range(source_start, length))
            for destination_start, source_start, length in seed_mapping
        ]
        for seed_mapping in seed_maps
    ]

    for seed_mapping in seed_mappings:
        mapping_applied_ranges: list[Range] = []
        for destination_start, mapping_range in seed_mapping:
            non_mapped: list[Range] = []
            for seed_numbers_range in seed_numbers_ranges:
                mapped_ranges, non_mapped_ranges = apply_mapping_range(
                    mapping_range, destination_start, seed_numbers_range
                )
                mapping_applied_ranges = [*mapping_applied_ranges, *mapped_ranges]
                non_mapped = [
                    *non_mapped,
                    *non_mapped_ranges,
                ]

            seed_numbers_ranges = non_mapped
        seed_numbers_ranges = [*seed_numbers_ranges, *mapping_applied_ranges]

    return min([rng.start for rng in seed_numbers_ranges])


print(
    f"""
    Day 05: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
