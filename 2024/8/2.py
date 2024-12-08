import fileinput
import math
from dataclasses import dataclass
from itertools import combinations

EMPTY = "."


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class Antenna:
    frequency: str
    position: Position


def trace_line(start_pos: Position, step_x: int, step_y: int, rows: int, cols: int) -> set[Position]:
    """Trace a line from the start position using the given steps until hitting grid bounds."""
    points = set()
    current_x = start_pos.x
    current_y = start_pos.y

    while 0 <= current_x < rows and 0 <= current_y < cols:
        points.add(Position(current_x, current_y))
        current_x += step_x
        current_y += step_y

    return points


def calculate_antinodes(antennas: list[Antenna], rows: int, cols: int) -> set[Position]:
    """Calculate all antinode positions for the given antennas."""
    antinodes = set()

    # Group antennas by frequency.
    antennas_by_frequency: dict[str, list[Position]] = {
        frequency: [antenna.position for antenna in antennas if antenna.frequency == frequency]
        for frequency in {antenna.frequency for antenna in antennas}
    }

    for antenna_positions in antennas_by_frequency.values():
        # Skip frequencies with less than 2 antennas since we need pairs.
        if len(antenna_positions) < 2:
            continue

        # Check all pairs of antennas.
        for position1, position2 in combinations(antenna_positions, 2):
            delta_x = position2.x - position1.x
            delta_y = position2.y - position1.y

            # Reduce to the smallest step increments.
            greatest_common_divisor = math.gcd(delta_x, delta_y)
            step_x = delta_x // greatest_common_divisor
            step_y = delta_y // greatest_common_divisor

            # Trace backward from position1.
            antinodes.update(trace_line(position1, -step_x, -step_y, rows, cols))

            # Trace forward from position1.
            forward_start = Position(position1.x + step_x, position1.y + step_y)
            antinodes.update(trace_line(forward_start, step_x, step_y, rows, cols))

    return antinodes


def parse_antennas(grid: list[list[str]], num_rows: int, num_cols: int) -> list[Antenna]:
    """Parse the grid to find all antennas and their positions."""
    return [
        Antenna(frequency=grid[x][y], position=Position(x, y))
        for x in range(num_rows)
        for y in range(num_cols)
        if grid[x][y] != EMPTY
    ]


def handler(raw_lines: fileinput.FileInput) -> int:
    grid = [list(line.strip()) for line in raw_lines]
    rows = len(grid)
    cols = len(grid[0])

    antennas = parse_antennas(grid, rows, cols)

    return len(calculate_antinodes(antennas, rows, cols))


if __name__ == "__main__":
    print(handler(fileinput.input()))
