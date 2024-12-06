import fileinput
from enum import IntEnum, auto


class Cell(auto):
    EMPTY = "."
    OBSTACLE = "#"


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class PatrolResult(IntEnum):
    EXIT = auto()
    LOOP = auto()


DIRECTION_VECTORS = {
    Direction.UP: (-1, 0),  # Move up: decrease row, same column
    Direction.RIGHT: (0, 1),  # Move right: same row, increase column
    Direction.DOWN: (1, 0),  # Move down: increase row, same column
    Direction.LEFT: (0, -1),  # Move left: same row, decrease column
}


def turn_right(direction_index: int) -> int:
    """Return the next direction when turning right."""
    if direction_index == Direction.LEFT:
        return Direction.UP

    return Direction(direction_index + 1)


def find_guard_start_and_direction(grid: list[str]) -> tuple[int, int, int]:
    """Find the guard's starting position and direction in the grid."""
    guard_symbol_to_direction = {"^": Direction.UP, ">": Direction.RIGHT, "v": Direction.DOWN, "<": Direction.LEFT}

    for row_index, row in enumerate(grid):
        for col_index, cell_value in enumerate(row):
            if cell_value in guard_symbol_to_direction:
                return (row_index, col_index, int(guard_symbol_to_direction[cell_value]))

    raise ValueError("No guard found in grid")


def simulate_patrol(grid: list[str], guard_row: int, guard_col: int, direction: int) -> PatrolResult:
    grid_height = len(grid)
    grid_width = len(grid[0])

    visited_states: set[tuple[int, int, int]] = set()
    visited_states.add((guard_row, guard_col, direction))

    while True:
        delta_row, delta_col = DIRECTION_VECTORS[Direction(direction)]
        next_row = guard_row + delta_row
        next_col = guard_col + delta_col

        # Check bounds
        if not (0 <= next_row < grid_height and 0 <= next_col < grid_width):
            # Guard leaves the grid.
            return PatrolResult.EXIT

        # Check obstacle
        if grid[next_row][next_col] == Cell.OBSTACLE:
            # Turn right
            direction = turn_right(direction)
        else:
            # Move forward
            guard_row, guard_col = next_row, next_col

            # Check if we've been in this state before.
            state = (guard_row, guard_col, direction)
            if state in visited_states:
                # Loop detected!
                return PatrolResult.LOOP

            visited_states.add(state)


def handler(raw_lines: fileinput.FileInput) -> int:
    grid = [line.strip() for line in raw_lines]
    grid_height = len(grid)
    grid_width = len(grid[0])

    guard_row, guard_col, guard_direction = find_guard_start_and_direction(grid)

    # Convert the grid into a mutable structure.
    mutable_grid = [list(row) for row in grid]

    # Find all possible positions to place a new obstruction. The cell
    # must be EMPTY and not the guard's starting position.
    loop_count = 0
    for current_row in range(grid_height):
        for current_col in range(grid_width):
            # Skip the guard's starting position.
            if (current_row, current_col) == (guard_row, guard_col):
                continue

            if mutable_grid[current_row][current_col] == Cell.EMPTY:
                # Place an obstruction.
                mutable_grid[current_row][current_col] = Cell.OBSTACLE

                # Run simulation.
                patrol_result = simulate_patrol(
                    ["".join(row) for row in mutable_grid], guard_row, guard_col, guard_direction
                )

                if patrol_result == PatrolResult.LOOP:
                    loop_count += 1

                # Remove obstruction
                mutable_grid[current_row][current_col] = Cell.EMPTY

    return loop_count


if __name__ == "__main__":
    print(handler(fileinput.input()))
