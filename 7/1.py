import fileinput
import re

from fileinput import FileInput
from typing import Dict, List, Tuple

GRAPH: Dict[str, List[Tuple[str, str]]] = {}
COLOR_TO_MATCH = "shiny gold"


def contains_shiny_gold_bag(color: str) -> bool:
    if color == COLOR_TO_MATCH:
        return True

    return any(contains_shiny_gold_bag(bag_color) for _, bag_color in GRAPH[color])


def handler(rules: FileInput) -> int:
    can_contain_count = 0

    for rule in rules:
        rule = rule.strip()

        # Extract the parent bag color and then all of the child bags
        # contained within it.
        match = re.match(r"([\w\s]+?) bags", rule)
        if match:
            parent_bag_color = match.group(1)
        child_bags_contained = re.findall(r"(\d+) ([\w\s]+?) bag", rule)

        GRAPH[parent_bag_color] = child_bags_contained

    # Increment for any bag that can contain a shiny gold bag.
    for parent in GRAPH.keys():
        can_contain_count += contains_shiny_gold_bag(parent)

    return can_contain_count - 1


if __name__ == "__main__":
    print(handler(fileinput.input()))
