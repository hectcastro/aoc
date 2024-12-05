import fileinput
import graphlib
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from fileinput import FileInput
from typing import List


class Section(Enum):
    ORDERING_RULES = 1
    UPDATES = 2


@dataclass
class OrderingRule:
    before: int
    after: int


def parse_ordering_rule(line: str) -> OrderingRule:
    x_str, y_str = line.strip().split("|")
    return OrderingRule(before=int(x_str), after=int(y_str))


def parse_ordering_rules_and_updates(raw_lines: FileInput) -> tuple[List[OrderingRule], List[str]]:
    """Parse the input into ordering rules and updates."""
    ordering_rules: List[OrderingRule] = []
    updates: List[str] = []
    section = Section.ORDERING_RULES

    for line in raw_lines:
        if line.strip() == "":
            section = Section.UPDATES
            continue
        if section == Section.ORDERING_RULES:
            if "|" in line:
                ordering_rules.append(parse_ordering_rule(line))
        else:
            updates.append(line.strip())

    return ordering_rules, updates


def reorder_and_get_middle_page(rules: list[OrderingRule]) -> int:
    """Reorders pages based on ordering rules and returns the middle page number."""
    dependencies: dict[int, set[int]] = defaultdict(set)

    # Add dependencies based on ordering rules.
    for rule in rules:
        dependencies[rule.after].add(rule.before)

    ts = graphlib.TopologicalSorter(dependencies)
    sorted_pages = list(ts.static_order())

    # Find the middle page number
    middle_index = len(sorted_pages) // 2

    return sorted_pages[middle_index]


def handler(raw_lines: FileInput) -> int:
    rules, updates = parse_ordering_rules_and_updates(raw_lines)
    total_middle_pages = 0

    for update_line in updates:
        update_pages = [int(x.strip()) for x in update_line.strip().split(",")]
        page_indices = {page: idx for idx, page in enumerate(update_pages)}
        correct_order = True
        relevant_rules = []

        # Collect all relevant rules and check if the update is correctly ordered
        for rule in rules:
            if rule.before in page_indices and rule.after in page_indices:
                relevant_rules.append(rule)
                if page_indices[rule.before] >= page_indices[rule.after]:
                    correct_order = False

        if not correct_order:
            middle_page = reorder_and_get_middle_page(relevant_rules)
            total_middle_pages += middle_page
        else:
            # Skip correctly ordered updates.
            pass

    return total_middle_pages


if __name__ == "__main__":
    print(handler(fileinput.input()))
