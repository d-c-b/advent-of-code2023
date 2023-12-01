from os import path

NUMBER_TEXT_TO_INTS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parse_input() -> list[str]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    return input_file.read().strip().splitlines()


def solve_part_1() -> int:
    lines = parse_input()
    calibration_values = []
    for line in lines:
        digits = [char for char in line if char.isdigit()]
        calibration_values.append(int(digits[0] + digits[-1]))
    return sum(calibration_values)


def check_for_text_or_digit_number(string: str) -> int | None:
    if string[0].isdigit():
        return int(string[0])

    for text_number in NUMBER_TEXT_TO_INTS:
        if string.startswith(text_number):
            return NUMBER_TEXT_TO_INTS[text_number]
    return None


def solve_part_2() -> int:
    lines = parse_input()
    calibration_values = []
    first = last = None
    for line in lines:
        for i in range(len(line)):
            first = check_for_text_or_digit_number(line[i:])
            if first:
                break

        for i in range(len(line) - 1, -1, -1):
            last = check_for_text_or_digit_number(line[i:])
            if last:
                break
        
        if not first or not last:
            raise Exception(f"No numbers found in line: {line}")

        calibration_values.append((first * 10) + last)

    return sum(calibration_values)


print(
    f"""
    Day 01: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
