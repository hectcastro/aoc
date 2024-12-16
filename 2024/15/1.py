import fileinput
from dataclasses import dataclass
from enum import Enum


class Cell(Enum):
    WALL = "#"
    ROBOT = "@"
    BOX = "O"


class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.row + other.row, self.col + other.col)


DIRECTIONS = {
    Direction.UP: Position(-1, 0),
    Direction.DOWN: Position(1, 0),
    Direction.LEFT: Position(0, -1),
    Direction.RIGHT: Position(0, 1),
}


def is_first_line_of_moves(line: str, map_width: int) -> bool:
    """Check if the line is the first line of moves."""
    return len(line) != map_width or ((not line.startswith(Cell.WALL.value)) and (not line.endswith(Cell.WALL.value)))


def parse_warehouse(lines: list[str]) -> tuple[list[list[str]], int]:
    """Parse the warehouse from the lines and return the warehouse and the index of the first line of moves."""
    map_width = len(lines[0])
    map_lines = []
    index = 0

    for index, line in enumerate(lines):
        if is_first_line_of_moves(line, map_width):
            break

        map_lines.append(line)

    warehouse = [list(row) for row in map_lines]

    return warehouse, index


def parse_moves(lines: list[str], moves_start_index: int) -> str:
    """Parse the moves from the lines and return the moves string."""
    return "".join(lines[moves_start_index:]).strip()


def find_initial_positions(warehouse: list[list[str]]) -> tuple[Position, set[Position]]:
    """Find initial robot and box positions in the warehouse."""
    warehouse_height = len(warehouse)
    warehouse_width = len(warehouse[0])

    robot_position = Position(0, 0)
    box_positions = set()

    for row in range(warehouse_height):
        for col in range(warehouse_width):
            pos = Position(row, col)
            if warehouse[row][col] == Cell.ROBOT.value:
                robot_position = pos
            if warehouse[row][col] == Cell.BOX.value:
                box_positions.add(pos)

    return robot_position, box_positions


def handler(raw_lines: fileinput.FileInput) -> int:
    lines = [line.rstrip("\n") for line in raw_lines]
    warehouse, moves_start_index = parse_warehouse(lines)
    moves = parse_moves(lines, moves_start_index)
    robot_position, box_positions = find_initial_positions(warehouse)

    def is_wall(pos: Position) -> bool:
        return warehouse[pos.row][pos.col] == Cell.WALL.value

    for move in moves:
        delta = DIRECTIONS[Direction(move)]
        next_position = robot_position + delta

        if is_wall(next_position):
            # Hit a wall!
            continue

        if next_position in box_positions:
            # We have a box; attempt chain pushing.
            boxes_to_push: list[Position] = []
            current_position = next_position

            # Collect all consecutive boxes in the direction of movement.
            while current_position in box_positions:
                boxes_to_push.append(current_position)
                current_position = current_position + delta

            # Now current_position is the spot after the last box in the chain.
            if is_wall(current_position) or current_position in box_positions:
                # No space to push!
                continue

            # Push all boxes forward.
            for box_position in reversed(boxes_to_push):
                box_positions.remove(box_position)
                box_positions.add(box_position + delta)

            # Move the robot into the position previously occupied by the first box.
            robot_position = next_position
        else:
            # Empty space, just move the robot.
            robot_position = next_position

    return sum(position.row * 100 + position.col for position in box_positions)


if __name__ == "__main__":
    print(handler(fileinput.input()))
