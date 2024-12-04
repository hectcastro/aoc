import fileinput
from fileinput import FileInput

VALID_DIAGONAL_WORDS = {"MAS", "SAM"}


def count_x_mas(grid: list[list[str]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    crossing_count = 0

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            # Get the northwest-southeast diagonal word centered at (row, col)
            northwest_southeast_positions = [(row - 1, col - 1), (row, col), (row + 1, col + 1)]
            northwest_southeast_word = "".join(grid[x][y] for x, y in northwest_southeast_positions)

            # Get the northeast-southwest diagonal word centered at (row, col)
            northeast_southwest_positions = [(row - 1, col + 1), (row, col), (row + 1, col - 1)]
            northeast_southwest_word = "".join(grid[x][y] for x, y in northeast_southwest_positions)

            if northwest_southeast_word in VALID_DIAGONAL_WORDS and northeast_southwest_word in VALID_DIAGONAL_WORDS:
                crossing_count += 1

    return crossing_count


def handler(raw_puzzle: FileInput) -> int:
    grid = [list(line.strip()) for line in raw_puzzle]

    return count_x_mas(grid)


if __name__ == "__main__":
    print(handler(fileinput.input()))
