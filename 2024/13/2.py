import fileinput
from dataclasses import dataclass

MAX_TRIES = 100 + 1
A_MULTIPLIER = 3
ERROR_OFFSET = 10000000000000


@dataclass
class Position:
    x: int
    y: int


def parse_line(line: str, is_prize: bool = False) -> Position:
    """Parse a line containing X, Y coordinates and return them as a Position."""
    parts = line.split(",")
    x_str = parts[0].split(":")[1].strip()
    y_str = parts[1].strip()

    if is_prize:
        x = int(x_str.replace("X=", ""))
        y = int(y_str.replace("Y=", ""))
    else:
        x = int(x_str.replace("X", "").replace("+", ""))
        y = int(y_str.replace("Y", "").replace("+", ""))

    return Position(x, y)


def is_integer(numerator: int, determinant: int) -> bool:
    """Check if a fraction represented by numerator/determinant results in an integer."""
    return numerator % determinant == 0


def handler(raw_lines: fileinput.FileInput) -> int:
    lines = [line.strip() for line in raw_lines if line.strip()]

    machine_count = len(lines) // 3
    total_min_cost = 0
    prizes_won = 0

    for i in range(machine_count):
        pos_a = parse_line(lines[3 * i])
        pos_b = parse_line(lines[3 * i + 1])
        pos_p = parse_line(lines[3 * i + 2], is_prize=True)

        # Add the required offset to the prize position.
        pos_p.x += ERROR_OFFSET
        pos_p.y += ERROR_OFFSET

        # Solve the linear equations:
        #   A_x * a + B_x * b = P_x
        #   A_y * a + B_y * b = P_y
        a_x, a_y = pos_a.x, pos_a.y
        b_x, b_y = pos_b.x, pos_b.y
        p_x, p_y = pos_p.x, pos_p.y

        determinant = a_x * b_y - a_y * b_x
        min_cost = None

        # Only proceed if we have a unique solution.
        if determinant != 0:
            numerator_a = p_x * b_y - p_y * b_x
            numerator_b = a_x * p_y - a_y * p_x

            # Check if a and b are integers.
            if is_integer(numerator_a, determinant) and is_integer(numerator_b, determinant):
                a = numerator_a // determinant
                b = numerator_b // determinant

                if a >= 0 and b >= 0:
                    cost = A_MULTIPLIER * a + b
                    min_cost = cost

        if min_cost:
            prizes_won += 1
            total_min_cost += min_cost

    return total_min_cost


if __name__ == "__main__":
    print(handler(fileinput.input()))
