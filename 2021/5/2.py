import sys
from collections import Counter, namedtuple
from typing import TextIO

LineSegment = namedtuple("LineSegment", ["x1", "y1", "x2", "y2"])


def parse_line_segment(line: str) -> LineSegment:
    start, end = line.split(" -> ")
    return LineSegment(*[int(coord) for coord in start.split(",")], *[int(coord) for coord in end.split(",")])


def handler(raw_line_segments: TextIO) -> int:
    line_segments = [parse_line_segment(line) for line in raw_line_segments]
    straight, diagonal = [], []

    for line_segment in line_segments:
        x1, y1, x2, y2 = line_segment
        (x1, y1), (x2, y2) = sorted([(x1, y1), (x2, y2)])

        if x1 == x2 or y1 == y2:
            straight += [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]
        elif y1 < y2:
            diagonal += [(x, y1 + idx) for idx, x in enumerate(range(x1, x2 + 1))]
        else:
            diagonal += [(x, y1 - idx) for idx, x in enumerate(range(x1, x2 + 1))]

    position_counts = Counter(straight) + Counter(diagonal)

    return sum(v > 1 for v in position_counts.values())


if __name__ == "__main__":
    print(handler(sys.stdin))
