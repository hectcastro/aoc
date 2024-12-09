import fileinput
from dataclasses import dataclass


@dataclass
class DiskLayout:
    file_lengths: list[int]
    free_lengths: list[int]
    disk_blocks: list[int]


def parse_disk_blocks(lengths: list[int]) -> DiskLayout:
    """Parse the input lengths into file lengths, free lengths, and disk blocks."""
    file_lengths, free_lengths, disk_blocks = [], [], []
    current_file_id = 0

    for index in range(0, len(lengths), 2):
        file_length = lengths[index]
        file_lengths.append(file_length)

        # Add file blocks.
        disk_blocks.extend([current_file_id] * file_length)

        # Check if there's a free length after this file.
        if index + 1 < len(lengths):
            free_space_length = lengths[index + 1]
            free_lengths.append(free_space_length)

            # Add free blocks.
            disk_blocks.extend([-1] * free_space_length)

        current_file_id += 1

    return DiskLayout(file_lengths, free_lengths, disk_blocks)


def compact_disk_blocks(disk_blocks: list[int]) -> None:
    """Compact disk blocks by moving file blocks to the left to fill free spaces."""
    while True:
        # Find the first free block.
        try:
            left_free_idx = disk_blocks.index(-1)
        except ValueError:
            # No free blocks found at all; already fully packed.
            break

        # Find the last file block from the right.
        right_file_idx = -1
        for i in range(len(disk_blocks) - 1, -1, -1):
            if disk_blocks[i] != -1:
                right_file_idx = i
                break

        # If the rightmost file block is to the left of the leftmost free space,
        # it means no compaction is needed.
        if right_file_idx < left_free_idx:
            break

        # Move that rightmost file block into the leftmost free space.
        disk_blocks[left_free_idx] = disk_blocks[right_file_idx]
        disk_blocks[right_file_idx] = -1


def calculate_checksum(disk_blocks: list[int]) -> int:
    """Calculate checksum by summing position * block_id for all file blocks."""
    checksum = 0

    for block_position, block_id in enumerate(disk_blocks):
        # Skip free blocks.
        if block_id >= 0:
            checksum += block_position * block_id

    return checksum


def handler(raw_lines: fileinput.FileInput) -> int:
    disk_map = next(raw_lines).strip()
    lengths = [int(x) for x in disk_map]

    disk_layout = parse_disk_blocks(lengths)
    compact_disk_blocks(disk_layout.disk_blocks)

    return calculate_checksum(disk_layout.disk_blocks)


if __name__ == "__main__":
    print(handler(fileinput.input()))
