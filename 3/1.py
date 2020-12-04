import fileinput

from fileinput import FileInput
from typing import List

MOVE_RIGHT_STEPS = 3
MOVE_DOWN_STEPS = 1


def expand_grid(patterns: FileInput) -> List[List[str]]:
    grid = []

    # Add all of the patterns as-is to a list. This pass
    # is necessary to determine how wide the grid should be.
    for pattern in patterns:
        grid.append(list(pattern.strip()))

    # Mutate the existing grid so that is of a width that can
    # support the number of moves necessary to get to the bottom.
    grid = [
        pattern * ((len(grid) // (len(pattern) // MOVE_RIGHT_STEPS)) + 1)
        for pattern in grid
    ]

    return grid


def handler(init_grid: FileInput) -> int:
    grid = expand_grid(init_grid)
    x, y = (0, 0)
    tree_collisions = 0

    # Terminate the loop when you get to one of the edges.
    while x != len(grid) - 1 and y != len(grid[0]) - 1:
        x += MOVE_DOWN_STEPS
        y += MOVE_RIGHT_STEPS

        if grid[x][y] == "#":
            grid[x][y] = "X"
            tree_collisions += 1
        else:
            grid[x][y] = "O"

    return tree_collisions


if __name__ == "__main__":
    print(handler(fileinput.input()))
