from os import path
from collections import Counter

CARD_VALUES_ORDER_ASC = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
)

HANDS_ORDERED_ASC = ("HC", "1P", "2P", "3K", "FH", "4K", "5K")


def parse_input() -> list[tuple[str, int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    rounds = [tuple(line.split()) for line in lines]
    return [(hand, int(bid)) for hand, bid in rounds]


def determine_hand(hand: str, wildcard: str | None) -> str:
    comparison_hand = hand

    if wildcard:
        if hand == wildcard * 5:
            return "5K"
        counted_raw = Counter(hand)
        most_common_non_wildcard_char = [
            char for char, _ in counted_raw.most_common() if char != wildcard
        ][0]
        comparison_hand = hand.replace(wildcard, most_common_non_wildcard_char)

    counted = Counter(comparison_hand)

    if len(counted) == 1:
        return "5K"

    if len(counted) == 2:
        if sorted(counted.values()) == [1, 4]:
            return "4K"
        elif sorted(counted.values()) == [2, 3]:
            return "FH"

    if len(counted) == 3:
        if sorted(counted.values()) == [1, 1, 3]:
            return "3K"
        elif sorted(counted.values()) == [1, 2, 2]:
            return "2P"

    if len(counted) == 4:
        return "1P"

    if len(counted) == 5:
        return "HC"

    raise Exception(f"Unable to determine hand type for hand: {hand}")


def sort_card_hands(
    unsorted_hands: list[tuple[str, int]], wildcard: str | None = None
) -> list[tuple[str, int]]:
    CARD_ORDER: tuple[str, ...] = CARD_VALUES_ORDER_ASC
    if wildcard:
        CARD_ORDER = tuple(
            [
                wildcard,
                *[card for card in CARD_VALUES_ORDER_ASC if card != wildcard],
            ]
        )

    sorted_hands: list[tuple[str, int]] = []
    for h in HANDS_ORDERED_ASC:
        hands_of_type = [
            (hand, bid)
            for hand, bid in unsorted_hands
            if determine_hand(hand, wildcard) == h
        ]
        hand_type_sorted_by_highest_card = sorted(
            hands_of_type,
            key=lambda hands: [CARD_ORDER.index(card) for card in hands[0]],
        )
        sorted_hands = [*sorted_hands, *hand_type_sorted_by_highest_card]

    return sorted_hands


def solve_part_1() -> int:
    rounds = parse_input()
    sorted_hands = sort_card_hands(rounds)
    return sum([bid * (i + 1) for i, (_, bid) in enumerate(sorted_hands)])


def solve_part_2() -> int:
    rounds = parse_input()
    sorted_hands = sort_card_hands(rounds, wildcard="J")
    return sum([bid * (i + 1) for i, (_, bid) in enumerate(sorted_hands)])


print(
    f"""
    Day 07: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
