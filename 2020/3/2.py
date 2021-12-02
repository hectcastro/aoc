import fileinput
import functools
import operator
from fileinput import FileInput
from typing import List

SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def expand_grid(template_grid: List[List[str]], right: int) -> List[List[str]]:
    grid = []

    # Mutate the existing grid so that is of a width that can
    # support the number of moves necessary to get to the bottom.
    grid = [
        pattern * ((len(template_grid) // (len(pattern) // right)) + 1)
        for pattern in template_grid
    ]

    return grid


def handler(init_grid: FileInput) -> int:
    template_grid = []

    # Add all of the patterns as-is to a list. This pass
    # is necessary to determine how wide the grid should be.
    for pattern in init_grid:
        template_grid.append(list(pattern.strip()))

    all_tree_collisions = []

    for right, down in SLOPES:
        grid = expand_grid(template_grid, right)
        x, y = (0, 0)
        tree_collisions = 0

        # Terminate the loop when you get to one of the edges.
        while x != len(grid) - 1 and y != len(grid[0]) - 1:
            x += down
            y += right

            if grid[x][y] == "#":
                grid[x][y] = "X"
                tree_collisions += 1
            else:
                grid[x][y] = "O"

        all_tree_collisions.append(tree_collisions)

    return functools.reduce(operator.mul, all_tree_collisions, 1)


if __name__ == "__main__":
    print(handler(fileinput.input()))
