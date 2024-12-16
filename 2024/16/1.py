import fileinput
from dataclasses import dataclass
from enum import Enum

import networkx as nx

INFINITY = float("inf")


class Cell(Enum):
    WALL = "#"
    START = "S"
    END = "E"


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn_left(self) -> "Direction":
        return Direction((self.value - 1) % 4)

    def turn_right(self) -> "Direction":
        return Direction((self.value + 1) % 4)

    @property
    def delta(self) -> tuple[int, int]:
        return DIRECTIONS[self]


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: tuple[int, int]) -> "Position":
        dr, dc = other
        return Position(self.row + dr, self.col + dc)

    def in_bounds(self, max_row: int, max_col: int) -> bool:
        return 0 <= self.row < max_row and 0 <= self.col < max_col


@dataclass(frozen=True)
class State:
    position: Position
    direction: Direction


DIRECTIONS = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}


def find_start_end_positions(maze: list[str], maze_height: int, maze_width: int) -> tuple[Position, Position]:
    """Find the start and end positions in the maze."""
    start_position = end_position = Position(0, 0)

    for row in range(maze_height):
        for col in range(maze_width):
            if maze[row][col] == Cell.START.value:
                start_position = Position(row, col)
            elif maze[row][col] == Cell.END.value:
                end_position = Position(row, col)

    return start_position, end_position


def build_graph(
    maze: list[str], maze_height: int, maze_width: int, start_position: Position, end_position: Position
) -> nx.DiGraph:
    """Build a directed graph representing possible moves in the maze."""
    graph: nx.DiGraph = nx.DiGraph()

    # Add nodes and edges for each valid position and direction.
    for row in range(maze_height):
        for col in range(maze_width):
            current_position = Position(row, col)

            if maze[row][col] == Cell.WALL.value:
                continue

            for direction in Direction:
                current_state = State(current_position, direction)

                # Add forward movement edge.
                next_position = current_position + direction.delta
                if (
                    next_position.in_bounds(maze_height, maze_width)
                    and maze[next_position.row][next_position.col] != Cell.WALL.value
                ):
                    next_state = State(next_position, direction)
                    graph.add_edge(current_state, next_state, weight=1)

                # Add turning edges.
                left_state = State(current_position, direction.turn_left())
                right_state = State(current_position, direction.turn_right())
                graph.add_edge(current_state, left_state, weight=1000)
                graph.add_edge(current_state, right_state, weight=1000)

    return graph


def find_shortest_path(
    maze: list[str],
    maze_height: int,
    maze_width: int,
    start_position: Position,
    end_position: Position,
) -> int:
    """Find the shortest path using networkx's Dijkstra algorithm."""
    graph = build_graph(maze, maze_height, maze_width, start_position, end_position)

    start_state = State(start_position, Direction.EAST)
    end_states = [State(end_position, direction) for direction in Direction]

    shortest_cost = INFINITY
    for end_state in end_states:
        path_length = int(nx.shortest_path_length(graph, start_state, end_state, weight="weight"))
        shortest_cost = min(shortest_cost, path_length)

    return int(shortest_cost) if shortest_cost != INFINITY else -1


def handler(raw_lines: fileinput.FileInput) -> int:
    maze = [line.rstrip("\n") for line in raw_lines]
    maze_height = len(maze)
    maze_width = len(maze[0])

    start_position, end_position = find_start_end_positions(maze, maze_height, maze_width)

    return find_shortest_path(maze, maze_height, maze_width, start_position, end_position)


if __name__ == "__main__":
    print(handler(fileinput.input()))
