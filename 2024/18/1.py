import fileinput
from collections import deque
from dataclasses import dataclass

GRID_SIZE = 71
MAX_COORDINATES = 1024

Grid = list[list[bool]]


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int

    def in_bounds(self, size: int) -> bool:
        return 0 <= self.row < size and 0 <= self.col < size

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.row + other.row, self.col + other.col)


MOVEMENT_DIRECTIONS = [
    Coordinate(0, 1),  # Right
    Coordinate(0, -1),  # Left
    Coordinate(1, 0),  # Down
    Coordinate(-1, 0),  # Up
]

START_POSITION = Coordinate(0, 0)
END_POSITION = Coordinate(GRID_SIZE - 1, GRID_SIZE - 1)


def initialize_corrupted_cells(raw_lines: fileinput.FileInput) -> Grid:
    """Initialize and return the grid of corrupted cells from the input coordinates."""
    corrupted_cells: Grid = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    coordinate_count = 0
    for line in raw_lines:
        if coordinate_count >= MAX_COORDINATES:
            break

        row, col = line.strip().split(",")
        coordinate = Coordinate(int(row), int(col))

        if coordinate.in_bounds(GRID_SIZE):
            corrupted_cells[coordinate.col][coordinate.row] = True

        coordinate_count += 1

    return corrupted_cells


def handler(raw_lines: fileinput.FileInput) -> int:
    corrupted_cells = initialize_corrupted_cells(raw_lines)

    # Check if start or end is corrupted.
    if corrupted_cells[START_POSITION.col][START_POSITION.row]:
        return -1
    if corrupted_cells[END_POSITION.col][END_POSITION.row]:
        return -1

    visited_cells = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    visited_cells[START_POSITION.col][START_POSITION.row] = True

    search_queue = deque([(START_POSITION, 0)])
    while search_queue:
        current_position, distance = search_queue.popleft()

        # If we've reached the end, return the total distance.
        if current_position == END_POSITION:
            return distance

        for direction in MOVEMENT_DIRECTIONS:
            next_position = current_position + direction

            # Check if next position is within grid bounds.
            if next_position.in_bounds(GRID_SIZE):
                # Only visit uncorrupted and unvisited cells.
                if (
                    not corrupted_cells[next_position.col][next_position.row]
                    and not visited_cells[next_position.col][next_position.row]
                ):
                    # Mark as visited and add to queue with incremented distance
                    visited_cells[next_position.col][next_position.row] = True
                    search_queue.append((next_position, distance + 1))

    return -1


if __name__ == "__main__":
    print(handler(fileinput.input()))
