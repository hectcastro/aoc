import fileinput
from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


DIRECTIONS = [d.value for d in Direction]


def in_bounds(row: int, col: int, rows: int, cols: int) -> bool:
    """Check if the given row and column indices are within the bounds of a grid."""
    return 0 <= row < rows and 0 <= col < cols


def explore_region(
    garden: list[list[str]], visited: list[list[bool]], start_row: int, start_col: int
) -> tuple[int, int]:
    """Explore the region starting from (start_row, start_col) using DFS."""
    positions_to_check = [(start_row, start_col)]
    plant_type = garden[start_row][start_col]
    region_positions = []
    num_rows = len(garden)
    num_cols = len(garden[0])

    # Identify the region cells.
    while positions_to_check:
        current_row, current_col = positions_to_check.pop()

        if visited[current_row][current_col]:
            continue

        visited[current_row][current_col] = True
        region_positions.append((current_row, current_col))

        for direction_row, direction_col in DIRECTIONS:
            neighbor_row = current_row + direction_row
            neighbor_col = current_col + direction_col

            if (
                in_bounds(neighbor_row, neighbor_col, num_rows, num_cols)
                and not visited[neighbor_row][neighbor_col]
                and garden[neighbor_row][neighbor_col] == plant_type
            ):
                positions_to_check.append((neighbor_row, neighbor_col))

    # Calculate area.
    region_area = len(region_positions)

    # Calculate perimeter.
    region_perimeter = 0
    for position_row, position_col in region_positions:
        for direction_row, direction_col in DIRECTIONS:
            neighbor_row = position_row + direction_row
            neighbor_col = position_col + direction_col

            # If neighbor is out of bounds or not the same type, increment perimeter
            if (
                not in_bounds(neighbor_row, neighbor_col, num_rows, num_cols)
                or garden[neighbor_row][neighbor_col] != plant_type
            ):
                region_perimeter += 1

    return region_area, region_perimeter


def calculate_total_cost(garden: list[list[str]]) -> int:
    """Calculate the total cost of fencing all regions in the given garden."""
    rows = len(garden)
    cols = len(garden[0])
    visited = [[False] * cols for _ in range(rows)]

    total_cost = 0
    for row in range(rows):
        for col in range(cols):
            if not visited[row][col]:
                area, perimeter = explore_region(garden, visited, row, col)

                total_cost += area * perimeter

    return total_cost


def handler(raw_lines: fileinput.FileInput) -> int:
    garden = [list(line.strip()) for line in raw_lines]

    return calculate_total_cost(garden)


if __name__ == "__main__":
    print(handler(fileinput.input()))
