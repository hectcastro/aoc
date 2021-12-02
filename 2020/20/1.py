import sys
import typing
from collections import Counter, defaultdict
from typing import Dict, List, TextIO


def tile_edges(tile):
    return [
        tile[0],
        tile[-1][::-1],
        "".join(map(lambda x: x[-1], tile)),
        "".join(map(lambda x: x[0], tile[::-1])),
    ]


def handler(raw_tiles: TextIO) -> int:
    tiles: Dict[int, List[str]] = defaultdict(list)
    raw_split_tiles = raw_tiles.read().split("\n\n")

    for raw_tile in raw_split_tiles:
        tile_id, tile = raw_tile.split(":")
        tiles[int(tile_id.replace("Tile ", ""))] = tile.lstrip().splitlines(False)

    edges: typing.Counter[int] = Counter()

    for t1 in tiles.values():
        edges.update(tile_edges(t1))
        edges.update(tile_edges(t1[::-1]))

    corner = 1

    for tid, t2 in tiles.items():
        unique = 0

        for edge in tile_edges(t2):
            if edges[edge] == 1:
                unique += 1

        if unique == 2:
            corner *= tid

    return corner


if __name__ == "__main__":
    print(handler(sys.stdin))
