import fileinput
from dataclasses import dataclass
from enum import Enum
from fileinput import FileInput


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


def parse_ordering_rules_and_updates(raw_lines: FileInput) -> tuple[list[OrderingRule], list[str]]:
    """Parse the input into ordering rules and updates."""
    ordering_rules: list[OrderingRule] = []
    updates: list[str] = []
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


def handler(raw_lines: FileInput) -> int:
    rules, updates = parse_ordering_rules_and_updates(raw_lines)

    total_middle_pages = 0
    for update_line in updates:
        update_pages = [int(x.strip()) for x in update_line.strip().split(",")]
        page_indices = {page: idx for idx, page in enumerate(update_pages)}
        correct_order = True

        for rule in rules:
            if rule.before in page_indices and rule.after in page_indices:
                if page_indices[rule.before] >= page_indices[rule.after]:
                    correct_order = False
                    # No need to check further if one rule is violated.
                    break

        # If update is in correct order; find the middle page number.
        if correct_order:
            middle_index = len(update_pages) // 2
            middle_page = update_pages[middle_index]
            total_middle_pages += middle_page

    return total_middle_pages


if __name__ == "__main__":
    print(handler(fileinput.input()))
