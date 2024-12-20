import fileinput
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Cell(Enum):
    WALL = "#"
    START = "S"
    END = "E"


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def in_bounds(self, max_row: int, max_col: int) -> bool:
        return 0 <= self.row < max_row and 0 <= self.col < max_col

    def is_wall(self, racetrack: list[list[str]]) -> bool:
        return racetrack[self.row][self.col] == Cell.WALL.value

    def is_track(self, racetrack: list[list[str]]) -> bool:
        return self.in_bounds(len(racetrack), len(racetrack[0])) and not self.is_wall(racetrack)

    def __add__(self, other: tuple[int, int]) -> "Position":
        dr, dc = other
        return Position(self.row + dr, self.col + dc)


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_start_and_end(
    racetrack: list[list[str]], rows: int, cols: int
) -> tuple[Optional[Position], Optional[Position]]:
    """Find start and end positions in the racetrack."""
    start_position: Optional[Position] = None
    end_position: Optional[Position] = None

    for row in range(rows):
        for col in range(cols):
            if racetrack[row][col] == Cell.START.value:
                start_position = Position(row, col)
            elif racetrack[row][col] == Cell.END.value:
                end_position = Position(row, col)

    return start_position, end_position


def bfs_dist(racetrack: list[list[str]], start: Position) -> list[list[int]]:
    """Compute distances from start position using BFS."""
    rows = len(racetrack)
    cols = len(racetrack[0])
    dist = [[-1] * cols for _ in range(rows)]
    positions_to_check: deque[Position] = deque()

    dist[start.row][start.col] = 0
    positions_to_check.append(start)

    while positions_to_check:
        current_position = positions_to_check.popleft()

        for direction in DIRECTIONS:
            next_position = current_position + direction

            if next_position.is_track(racetrack) and dist[next_position.row][next_position.col] == -1:
                dist[next_position.row][next_position.col] = dist[current_position.row][current_position.col] + 1
                positions_to_check.append(next_position)

    return dist


def handler(input_lines: fileinput.FileInput) -> int:
    racetrack = [list(line.rstrip("\n")) for line in input_lines]
    racetrack_height = len(racetrack)
    racetrack_width = len(racetrack[0])

    start_position, end_position = find_start_and_end(racetrack, racetrack_height, racetrack_width)

    if start_position is None or end_position is None:
        return 0

    distances_from_start = bfs_dist(racetrack, start_position)
    distances_from_end = bfs_dist(racetrack, end_position)
    shortest_path_length = distances_from_start[end_position.row][end_position.col]

    if shortest_path_length == -1:
        # No normal path exists.
        return 0

    # Consider all possible cheat positions.
    valid_shortcuts = set()
    for row in range(racetrack_height):
        for col in range(racetrack_width):
            current_position = Position(row, col)

            if distances_from_start[row][col] == -1:
                # Not reachable from start normally.
                continue

            # Try all possible two-step jumps from this position.
            for first_delta_row, first_delta_col in DIRECTIONS:
                intermediate_position = current_position + (first_delta_row, first_delta_col)

                if not intermediate_position.in_bounds(racetrack_height, racetrack_width):
                    continue

                for second_delta_row, second_delta_col in DIRECTIONS:
                    landing_position = intermediate_position + (second_delta_row, second_delta_col)

                    if not landing_position.is_track(racetrack):
                        continue

                    if distances_from_end[landing_position.row][landing_position.col] != -1:
                        shortcut_length = (
                            distances_from_start[row][col]
                            + 2
                            + distances_from_end[landing_position.row][landing_position.col]
                        )

                        if shortest_path_length - shortcut_length >= 100:
                            valid_shortcuts.add((current_position, landing_position))

    return len(valid_shortcuts)


if __name__ == "__main__":
    print(handler(fileinput.input()))
