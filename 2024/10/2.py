import fileinput
from dataclasses import dataclass
from enum import Enum
from functools import cache


@dataclass(frozen=True)
class Position:
    row: int
    col: int


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def parse_topographic_map(raw_lines: fileinput.FileInput) -> list[list[int]]:
    """Parses the raw input into a grid of integers representing the topographic map."""
    return [[int(c) for c in line.strip()] for line in raw_lines]


def get_neighbors(position: Position, num_rows: int, num_cols: int) -> list[Position]:
    """Returns valid neighbors for a given position."""
    neighbor_positions = [
        Position(position.row + delta_row, position.col + delta_col)
        for delta_row, delta_col in [d.value for d in Direction]
    ]

    return [pos for pos in neighbor_positions if 0 <= pos.row < num_rows and 0 <= pos.col < num_cols]


def compute_trailhead_rating(topographic_map: list[list[int]], start_position: Position) -> int:
    """Computes the rating for a trailhead."""
    rows = len(topographic_map)
    columns = len(topographic_map[0])

    @cache
    def dfs(position: Position) -> int:
        """Performs DFS to count paths to height 9."""
        current_elevation = topographic_map[position.row][position.col]

        if current_elevation == 9:
            return 1  # Base case: reached height 9

        total_paths = 0
        for neighbor in get_neighbors(position, rows, columns):
            neighbor_elevation = topographic_map[neighbor.row][neighbor.col]

            if neighbor_elevation == current_elevation + 1:
                total_paths += dfs(neighbor)

        return total_paths

    return dfs(start_position)


def handler(raw_lines: fileinput.FileInput) -> int:
    topographic_map = parse_topographic_map(raw_lines)
    rows = len(topographic_map)
    columns = len(topographic_map[0])
    total_rating = 0

    for row in range(rows):
        for col in range(columns):
            if topographic_map[row][col] == 0:
                # Found a trailhead
                total_rating += compute_trailhead_rating(topographic_map, Position(row, col))

    return total_rating


if __name__ == "__main__":
    print(handler(fileinput.input()))
