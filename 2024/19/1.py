import fileinput


def can_form_design(design: str, towel_patterns: set[str]) -> bool:
    """Check if the given design can be formed by concatenating any number of the patterns in towel_patterns."""
    design_length = len(design)
    can_form_up_to: list[bool] = [False] * (design_length + 1)
    can_form_up_to[0] = True

    for current_index in range(design_length):
        if can_form_up_to[current_index]:
            # If the design can be formed up to current_index, try appending each towel pattern.
            for pattern in towel_patterns:
                pattern_length = len(pattern)
                end_index = current_index + pattern_length

                # Check if the pattern fits and matches the substring in the design.
                if end_index <= design_length and design[current_index:end_index] == pattern:
                    can_form_up_to[end_index] = True

                    if can_form_up_to[design_length]:
                        # If the entire design can be formed, exit early.
                        return True

    return can_form_up_to[design_length]


def parse_towel_patterns(patterns: str) -> set[str]:
    """Parse a comma-separated line of towel patterns into a set of patterns."""
    return set(pattern.strip() for pattern in patterns.split(","))


def handler(raw_lines: fileinput.FileInput) -> int:
    lines = [line.strip() for line in raw_lines]

    towel_patterns = parse_towel_patterns(lines[0])

    designs_begin_index = 2
    designs = lines[designs_begin_index:]

    possible_count = 0
    for design in designs:
        if can_form_design(design, towel_patterns):
            possible_count += 1

    return possible_count


if __name__ == "__main__":
    print(handler(fileinput.input()))
