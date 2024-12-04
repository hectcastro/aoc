import fileinput
from fileinput import FileInput

WORD = "XMAS"


def count_word_in_grid(grid: list[list[str]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    word_length = len(WORD)
    occurrences = 0

    # Define all 8 possible directions to search
    search_directions = [
        (-1, 0),  # North
        (-1, 1),  # Northeast
        (0, 1),  # East
        (1, 1),  # Southeast
        (1, 0),  # South
        (1, -1),  # Southwest
        (0, -1),  # West
        (-1, -1),  # Northwest
    ]

    def is_position_in_bounds(row: int, col: int) -> bool:
        return 0 <= row < rows and 0 <= col < cols

    for start_row in range(rows):
        for start_col in range(cols):
            for direction_row, direction_col in search_directions:
                word_found = True

                for char_index in range(word_length):
                    current_row = start_row + direction_row * char_index
                    current_col = start_col + direction_col * char_index

                    if (
                        not is_position_in_bounds(current_row, current_col)
                        or grid[current_row][current_col] != WORD[char_index]
                    ):
                        word_found = False
                        break

                if word_found:
                    occurrences += 1

    return occurrences


def handler(raw_puzzle: FileInput) -> int:
    grid = [list(line.strip()) for line in raw_puzzle]

    return count_word_in_grid(grid)


if __name__ == "__main__":
    print(handler(fileinput.input()))
