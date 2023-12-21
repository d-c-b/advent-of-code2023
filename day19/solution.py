from os import path
import re


def parse_input() -> (
    tuple[
        dict[str, list[tuple[tuple[str, str, int] | None, str]]], list[dict[str, int]]
    ]
):
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    workflows_lines, parts_lines = input_file.read().strip().split("\n\n")

    workflows: dict[str, list[tuple[tuple[str, str, int] | None, str]]] = {}
    for workflow_line in workflows_lines.split("\n"):
        name, operations = workflow_line[:-1].split("{")
        workflows[name] = []

        for operation_string in operations.split(","):
            if ":" in operation_string:
                condition, next_workflow = operation_string.split(":")
                att, op, val = re.split(r"(<|>)", condition)
                workflows[name].append(((att, op, int(val)), next_workflow))

            else:
                workflows[name].append((None, operation_string))

    parts = [
        {
            attr: int(val)
            for attr, val in [a.split("=") for a in part_line.strip("{}").split(",")]
        }
        for part_line in parts_lines.split("\n")
    ]

    return workflows, parts


def find_next_workflow(
    part: dict[str, int], workflow: list[tuple[tuple[str, str, int] | None, str]]
) -> str:
    for rule in workflow:
        comparison_operation, next_workflow_name = rule
        if not comparison_operation:
            return next_workflow_name

        else:
            attribute, comparator, comparison_val = comparison_operation
            match comparator:
                case "<":
                    if part[attribute] < comparison_val:
                        return next_workflow_name

                case ">":
                    if part[attribute] > comparison_val:
                        return next_workflow_name
    raise Exception(
        f"Failed to match part: {part} to new workflow when running workflow {workflow}"
    )


def part_accepted(
    part: dict[str, int],
    name: str,
    workflows: dict[str, list[tuple[tuple[str, str, int] | None, str]]],
) -> bool:
    next_worfklow_name = find_next_workflow(part, workflows[name])

    match next_worfklow_name:
        case "A":
            return True

        case "R":
            return False

        case _:
            return part_accepted(part, next_worfklow_name, workflows)


def solve_part_1() -> int:
    workflows, parts = parse_input()
    accepted_parts = [part for part in parts if part_accepted(part, "in", workflows)]
    return sum([sum([v for v in part.values()]) for part in accepted_parts])


def combination_count_for_range(range_vals: dict[str, tuple[int, int]]) -> int:
    val = 1
    for attribute in "xmas":
        lower, upper = range_vals[attribute]
        val *= upper + 1 - lower
    return val


def count_accepted_combinations_for_ranges(
    range_values: dict[str, tuple[int, int]],
    workflows: dict[str, list[tuple[tuple[str, str, int] | None, str]]],
    workflow_name: str,
) -> int:
    if workflow_name == "A":
        return combination_count_for_range(range_values)
    if workflow_name == "R":
        return 0

    count = 0
    remaining_range_values = {**range_values}

    for operation in workflows[workflow_name]:
        op, next_workflow = operation
        if not op:
            count += count_accepted_combinations_for_ranges(
                remaining_range_values, workflows, next_workflow
            )

        else:
            attribute, comparator, comparison_val = op
            low, high = remaining_range_values[attribute]
            match comparator:
                case "<":
                    if low > comparison_val:
                        count += 0

                    else:
                        range_values_true_condition = {
                            **remaining_range_values,
                            attribute: (low, min(comparison_val - 1, high)),
                        }
                        count += count_accepted_combinations_for_ranges(
                            range_values_true_condition, workflows, next_workflow
                        )
                        if high > comparison_val:
                            remaining_range_values = {
                                **remaining_range_values,
                                attribute: (max(comparison_val, low), high),
                            }
                case ">":
                    if high < comparison_val:
                        count += 0

                    else:
                        range_values_true_condition = {
                            **remaining_range_values,
                            attribute: (max(comparison_val + 1, low), high),
                        }
                        count += count_accepted_combinations_for_ranges(
                            range_values_true_condition, workflows, next_workflow
                        )

                        if low < comparison_val:
                            remaining_range_values = {
                                **remaining_range_values,
                                attribute: (low, comparison_val),
                            }

    return count


def solve_part_2() -> int:
    workflows, _ = parse_input()
    accepted_combinations_count = count_accepted_combinations_for_ranges(
        {
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
        },
        workflows,
        "in",
    )

    return accepted_combinations_count


print(
    f"""
    Day 19: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
