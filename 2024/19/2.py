import fileinput


def count_ways_to_form_design(design: str, towel_patterns: set[str]) -> int:
    """Count the number of ways to form the given design by concatenating any number of the patterns."""
    design_length = len(design)
    ways: list[int] = [0] * (design_length + 1)
    ways[0] = 1

    for current_index in range(design_length):
        if ways[current_index] > 0:
            # If we have ways to form the design up to current_index, try each towel pattern.
            for pattern in towel_patterns:
                pattern_length = len(pattern)
                end_index = current_index + pattern_length

                # Check if the pattern fits here.
                if end_index <= design_length and design[current_index:end_index] == pattern:
                    ways[end_index] += ways[current_index]

    return ways[design_length]


def parse_towel_patterns(patterns: str) -> set[str]:
    """Parse a comma-separated line of towel patterns into a set of patterns."""
    return set(pattern.strip() for pattern in patterns.split(",") if pattern.strip())


def handler(raw_lines: fileinput.FileInput) -> int:
    lines = [line.strip() for line in raw_lines]

    towel_patterns = parse_towel_patterns(lines[0])

    designs_begin_index = 2
    designs = lines[designs_begin_index:]

    total_ways = 0
    for design in designs:
        total_ways += count_ways_to_form_design(design, towel_patterns)

    return total_ways


if __name__ == "__main__":
    print(handler(fileinput.input()))
