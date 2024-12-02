import fileinput
from fileinput import FileInput
from typing import List


def calc_differences(levels: List[int]) -> List[int]:
    """Calculate the differences between adjacent numbers in a list."""
    return [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]


def is_safe_report(levels: List[int]) -> bool:
    differences = calc_differences(levels)

    # Check for zero differences (adjacent levels cannot be equal)
    if 0 in differences:
        return False

    # Check if all differences are positive (increasing) or all negative (decreasing)
    is_increasing = all(d > 0 for d in differences)
    is_decreasing = all(d < 0 for d in differences)

    if not (is_increasing or is_decreasing):
        return False

    # Check if all absolute differences are between 1 and 3 inclusive
    if all(1 <= abs(d) <= 3 for d in differences):
        return True
    else:
        return False


def is_safe_with_dampener(levels: List[int]) -> bool:
    for i in range(len(levels)):
        adjusted_levels = levels[:i] + levels[i + 1 :]

        if len(adjusted_levels) < 2:
            continue

        if is_safe_report(adjusted_levels):
            return True

    return False


def handler(raw_reports: FileInput) -> int:
    safe_reports = 0

    for raw_report in raw_reports:
        report = raw_report.strip()
        levels = [int(x) for x in report.split()]

        if is_safe_report(levels) or is_safe_with_dampener(levels):
            safe_reports += 1

    return safe_reports


if __name__ == "__main__":
    print(handler(fileinput.input()))
