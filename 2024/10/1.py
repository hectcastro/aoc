import fileinput
from collections import deque
from dataclasses import dataclass
from enum import Enum


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


def compute_trailhead_score(topographic_map: list[list[int]], start_position: Position) -> int:
    """Computes the score for a single trailhead."""
    rows = len(topographic_map)
    columns = len(topographic_map[0])

    positions_to_check = deque([start_position])
    visited_positions: set[Position] = {start_position}
    reachable_peak_positions: set[Position] = set()

    while positions_to_check:
        current_pos = positions_to_check.popleft()
        current_elevation = topographic_map[current_pos.row][current_pos.col]

        for neighbor_pos in get_neighbors(current_pos, rows, columns):
            if neighbor_pos in visited_positions:
                continue

            neighbor_elevation = topographic_map[neighbor_pos.row][neighbor_pos.col]

            if neighbor_elevation == current_elevation + 1:
                visited_positions.add(neighbor_pos)
                positions_to_check.append(neighbor_pos)

                if neighbor_elevation == 9:
                    reachable_peak_positions.add(neighbor_pos)

    return len(reachable_peak_positions)


def handler(raw_lines: fileinput.FileInput) -> int:
    topographic_map = parse_topographic_map(raw_lines)
    max_x = len(topographic_map)
    max_y = len(topographic_map[0])
    total_score = 0

    for x in range(max_x):
        for y in range(max_y):
            if topographic_map[x][y] == 0:
                # Found a trailhead.
                total_score += compute_trailhead_score(topographic_map, Position(x, y))

    return total_score


if __name__ == "__main__":
    print(handler(fileinput.input()))
