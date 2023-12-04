from os import path


def parse_input() -> dict[int, list[list[int]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    input_lines = input_file.read().strip().splitlines()
    parsed = {}
    for line in input_lines:
        card_number, numbers = line.split(": ")
        card_id = int(card_number.strip().split()[1])
        winning, result = [
            [int(num) for num in number_string.split()]
            for number_string in numbers.split(" | ")
        ]
        parsed[card_id] = [winning, result]
    return parsed


def solve_part_1() -> int:
    scratchcards = parse_input()
    scratchcard_sum = 0

    for scratchcard, result in scratchcards.values():
        winning_numbers = [n for n in result if n in scratchcard]
        if len(winning_numbers) > 0:
            scratchcard_sum += 2 ** (len(winning_numbers) - 1)

    return scratchcard_sum


def solve_part_2() -> int:
    scratchcards = parse_input()
    copies_of_card_ids = {card_id: 1 for card_id in scratchcards.keys()}

    for id, (scratchcard, result) in scratchcards.items():
        winning_numbers = [n for n in result if n in scratchcard]
        if len(winning_numbers) > 0:
            for _ in range(copies_of_card_ids[id]):
                for i in range(id + 1, len(winning_numbers) + id + 1):
                    if i in copies_of_card_ids:
                        copies_of_card_ids[i] += 1

    return sum(copies_of_card_ids.values())


print(
    f"""
    Day 04: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
