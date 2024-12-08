import fileinput
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
        for pos1, pos2 in combinations(antenna_positions, 2):
            dx = pos2.x - pos1.x
            dy = pos2.y - pos1.y

            # Check antinodes at twice the distance.
            antinode1 = Position(pos1.x - dx, pos1.y - dy)
            antinode2 = Position(pos2.x + dx, pos2.y + dy)

            # Add valid antinodes within the bounds.
            if 0 <= antinode1.x < rows and 0 <= antinode1.y < cols:
                antinodes.add(antinode1)
            if 0 <= antinode2.x < rows and 0 <= antinode2.y < cols:
                antinodes.add(antinode2)

    # Only include the antennas themselves if they overlap with an existing antinode
    for antenna in antennas:
        if antenna.position in antinodes:
            antinodes.add(antenna.position)

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
