from os import path
from fractions import Fraction

MIN_VAL = 200_000_000_000_000
MAX_VAL = 400_000_000_000_000


def parse_input() -> list[tuple[list[int], list[int]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()

    hail_stones = []
    for line in lines:
        position_sring, velocity_string = line.split("@")
        position_coords = [int(p) for p in position_sring.strip().split(", ")]
        velocity_coords = [int(v) for v in velocity_string.strip().split(", ")]
        hail_stones.append((position_coords, velocity_coords))
    return hail_stones


def solve_part_1() -> int:
    hail_stones = parse_input()
    count = 0
    for i, (p1, v1) in enumerate(hail_stones):
        (px1, py1, _), (vx1, vy1, _) = p1, v1
        for j in range(i + 1, len(hail_stones)):
            (px2, py2, _), (vx2, vy2, _) = hail_stones[j]
            det = vx2 * vy1 - vx1 * vy2

            if det == 0:
                continue

            t1 = (-vy2 * (px2 - px1) + vx2 * (py2 - py1)) / det
            t2 = (-vy1 * (px2 - px1) + vx1 * (py2 - py1)) / det

            if t1 > 0 and t2 > 0:
                x, y = px1 + vx1 * t1, py1 + vy1 * t1
                if MIN_VAL < x < MAX_VAL and MIN_VAL < y < MAX_VAL:
                    count += 1

    return count


def create_matrix_rows_for_hailstone_pair(
    hailstone_i: tuple[list[int], list[int]],
    hailstone_j: tuple[list[int], list[int]],
) -> tuple[list[list[int]], list[int]]:
    (pxi, pyi, pzi), (vxi, vyi, vzi) = hailstone_i
    (pxj, pyj, pzj), (vxj, vyj, vzj) = hailstone_j

    x_y_row = [vyj - vyi, vxi - vxj, 0, pyi - pyj, pxj - pxi, 0]
    sol_xy = pxj * vyj - pyj * vxj + pyi * vxi - pxi * vyi

    x_z_row = [vzj - vzi, 0, vxi - vxj, pzi - pzj, 0, pxj - pxi]
    sol_xz = pxj * vzj - pzj * vxj + pzi * vxi - pxi * vzi

    y_z_row = [0, vzj - vzi, vyi - vyj, 0, pzi - pzj, pyj - pyi]
    sol_yz = pyj * vzj - pzj * vyj + pzi * vyi - pyi * vzi

    matrix_rows = [x_y_row, x_z_row, y_z_row]
    solution_vector = [sol_xy, sol_xz, sol_yz]

    return matrix_rows, solution_vector


def gaussian_elimination(
    matrix: list[list[int]],
) -> list[list[Fraction]]:
    rows, columns = len(matrix), len(matrix[0])
    current_row, current_column = 0, 0
    reduced_matrix = [[Fraction(x) for x in row] for row in matrix]

    while current_row < rows and current_column < rows - 1:
        i_max = 0
        for i in range(current_row, rows):
            if abs(reduced_matrix[i][current_column]) > abs(
                reduced_matrix[i_max][current_column]
            ):
                i_max = i

        if reduced_matrix[i_max][current_column] == 0:
            current_column += 1
            continue

        reduced_matrix[i_max], reduced_matrix[current_row] = (
            reduced_matrix[current_row],
            reduced_matrix[i_max],
        )

        for i in range(current_row + 1, rows):
            factor = (
                reduced_matrix[i][current_column]
                / reduced_matrix[current_row][current_column]
            )
            reduced_matrix[i][current_column] = Fraction(0)
            for j in range(current_column + 1, columns):
                reduced_matrix[i][j] = (
                    reduced_matrix[i][j] - reduced_matrix[current_row][j] * factor
                )

        current_row += 1
        current_column += 1

    return reduced_matrix


def get_solution_vector(reduced_matrix: list[list[Fraction]]) -> list[float]:
    solution_vector = [float(0) for _ in range(len(reduced_matrix))]

    for row in reversed(reduced_matrix):
        for index, col in enumerate(row):
            if col == 0:
                continue
            var, *coefficients, val = row[index:]
            solution_vector[index] = (
                val
                - sum(
                    [
                        solution_vector[n] * coefficient
                        for n, coefficient in enumerate(coefficients, start=index + 1)
                    ]
                )
            ) / var
            break

    return solution_vector


def solve_part_2() -> int:
    hail_stones = parse_input()

    matrix_rows_1, solution_vec_1 = create_matrix_rows_for_hailstone_pair(
        hail_stones[0], hail_stones[1]
    )
    matrix_rows_2, solution_vec_2 = create_matrix_rows_for_hailstone_pair(
        hail_stones[0], hail_stones[2]
    )

    full_matrix = [*matrix_rows_1, *matrix_rows_2]
    solution_vector = [*solution_vec_1, *solution_vec_2]

    augmented_matrix = [[*row, sol] for row, sol in zip(full_matrix, solution_vector)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    solution = get_solution_vector(reduced_matrix)

    *rock_position_coords, _, _, _ = solution
    return sum(int(coord) for coord in rock_position_coords)


print(
    f"""
    Day 24: 
    Part 1 Solution: {solve_part_1()}
    Part 2 Solution: {solve_part_2()}
    """
)
