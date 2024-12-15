import fileinput
from dataclasses import dataclass

WIDTH = 101
HEIGHT = 103
MIDDLE_X = 50
MIDDLE_Y = 51
TIME_TO_SIMULATE = 100


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Velocity:
    x: int
    y: int


def parse_coordinate_pair(raw_coord: str) -> tuple[int, int]:
    coord_str = raw_coord.split("=")[1]
    x_str, y_str = coord_str.split(",")

    return int(x_str), int(y_str)


def parse_input_lines(raw_lines: fileinput.FileInput) -> tuple[list[Position], list[Velocity]]:
    positions = []
    velocities = []

    for line in raw_lines:
        line = line.strip()

        parts = line.split()
        raw_position = parts[0]
        raw_velocity = parts[1]

        px, py = parse_coordinate_pair(raw_position)
        vx, vy = parse_coordinate_pair(raw_velocity)

        positions.append(Position(px, py))
        velocities.append(Velocity(vx, vy))

    return positions, velocities


def handler(raw_lines: fileinput.FileInput) -> int:
    positions, velocities = parse_input_lines(raw_lines)

    # Simulate each robot's position after 100 seconds.
    final_positions: list[Position] = []
    for position, velocity in zip(positions, velocities):
        x = (position.x + velocity.x * TIME_TO_SIMULATE) % WIDTH
        y = (position.y + velocity.y * TIME_TO_SIMULATE) % HEIGHT

        final_positions.append(Position(x, y))

    q1_count = 0
    q2_count = 0
    q3_count = 0
    q4_count = 0

    for position in final_positions:
        # Exclude robots on the middle lines.
        if position.x == MIDDLE_X or position.y == MIDDLE_Y:
            continue

        if position.x > MIDDLE_X and position.y < MIDDLE_Y:
            q1_count += 1
        elif position.x < MIDDLE_X and position.y < MIDDLE_Y:
            q2_count += 1
        elif position.x < MIDDLE_X and position.y > MIDDLE_Y:
            q3_count += 1
        elif position.x > MIDDLE_X and position.y > MIDDLE_Y:
            q4_count += 1

    return q1_count * q2_count * q3_count * q4_count


if __name__ == "__main__":
    print(handler(fileinput.input()))
