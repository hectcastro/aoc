import fileinput
from dataclasses import dataclass

MAX_TRIES = 100 + 1
A_MULTIPLIER = 3


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


def handler(raw_lines: fileinput.FileInput) -> int:
    lines = [line.strip() for line in raw_lines if line.strip()]

    machine_count = len(lines) // 3
    total_min_cost = 0
    prizes_won = 0

    for i in range(machine_count):
        pos_a = parse_line(lines[3 * i])
        pos_b = parse_line(lines[3 * i + 1])
        pos_p = parse_line(lines[3 * i + 2], is_prize=True)

        min_cost = None
        # Try all combinations of button presses up to MAX_TRIES.
        for a in range(MAX_TRIES):
            for b in range(MAX_TRIES):
                # Calculate final position after pressing buttons.
                x_pos = pos_a.x * a + pos_b.x * b
                y_pos = pos_a.y * a + pos_b.y * b

                if x_pos == pos_p.x and y_pos == pos_p.y:
                    # Calculate total cost.
                    cost = A_MULTIPLIER * a + b

                    # Keep track of minimum cost found.
                    if not min_cost or cost < min_cost:
                        min_cost = cost

        if min_cost:
            prizes_won += 1
            total_min_cost += min_cost

    return total_min_cost


if __name__ == "__main__":
    print(handler(fileinput.input()))
