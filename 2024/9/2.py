import fileinput
from dataclasses import dataclass
from typing import Optional


@dataclass
class DiskLayout:
    file_lengths: list[int]
    free_lengths: list[int]
    disk_blocks: list[int]


@dataclass
class FileInfo:
    file_id: int
    length: int


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
        else:
            # No free space after the last file
            free_lengths.append(0)

        current_file_id += 1

    return DiskLayout(file_lengths, free_lengths, disk_blocks)


def find_file_location(disk_blocks: list[int], file: FileInfo) -> tuple[Optional[int], Optional[int]]:
    """Find the start and end indices of a file in disk_blocks."""
    file_start_index = None
    file_end_index = None
    blocks_found = 0

    for block_index, block_value in enumerate(disk_blocks):
        if block_value == file.file_id:
            # Found a block belonging to our target file.
            blocks_found += 1
            if file_start_index is None:
                # If this is the first block found, mark the start.
                file_start_index = block_index
            if blocks_found == file.length:
                # If we've found all blocks, mark the end.
                file_end_index = block_index
                break

    return file_start_index, file_end_index


def find_free_segment(disk_blocks: list[int], file_length: int, before_index: int) -> Optional[int]:
    """Find leftmost free segment of sufficient length before the given index."""
    consecutive_free_blocks = 0
    segment_start_index = None

    for block_index in range(before_index):
        if disk_blocks[block_index] == -1:
            # Found a free block.
            if segment_start_index is None:
                # Mark start of new free segment.
                segment_start_index = block_index

            consecutive_free_blocks += 1

            if consecutive_free_blocks == file_length:
                # Found segment large enough for file.
                return segment_start_index
        else:
            # Hit a non-free block, reset our counters.
            segment_start_index = None
            consecutive_free_blocks = 0

    return None


def move_file_to_segment(
    disk_blocks: list[int], file: FileInfo, source_start: int, source_end: int, destination_start: int
) -> None:
    """Move a file from its current location to the target segment."""
    # Clear the old file location.
    for block_index in range(source_start, source_end + 1):
        disk_blocks[block_index] = -1

    # Place the file blocks at the target segment.
    for block_offset in range(file.length):
        disk_blocks[destination_start + block_offset] = file.file_id


def move_files_whole(disk_blocks: list[int], file_lengths: list[int]) -> None:
    """
    Attempt to move whole files to the leftmost free space block large enough to fit the entire file.
    """
    file_objects = [FileInfo(file_id, length) for file_id, length in enumerate(file_lengths)]
    # Sort files by ID in descending order to process larger IDs first.
    file_objects.sort(key=lambda file_object: file_object.file_id, reverse=True)

    for current_file in file_objects:
        current_start, current_end = find_file_location(disk_blocks, current_file)
        if current_start is None:
            continue

        leftmost_free_position = find_free_segment(disk_blocks, current_file.length, current_start)
        if leftmost_free_position is not None and current_end is not None:
            move_file_to_segment(disk_blocks, current_file, current_start, current_end, leftmost_free_position)


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
    move_files_whole(disk_layout.disk_blocks, disk_layout.file_lengths)

    return calculate_checksum(disk_layout.disk_blocks)


if __name__ == "__main__":
    print(handler(fileinput.input()))
