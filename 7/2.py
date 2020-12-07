import fileinput
import re

from fileinput import FileInput
from typing import Dict, List, Tuple

GRAPH: Dict[str, List[Tuple[str, str]]] = {}
COLOR_TO_MATCH = "shiny gold"


def bags_required(bag: str) -> int:
    bags_required_count = 0

    # Recursively determine the count of required bags.
    for bag_count, bag_color in GRAPH[bag]:
        bags_required_count += int(bag_count) * bags_required(bag_color)

    return 1 + bags_required_count


def handler(rules: FileInput) -> int:
    for rule in rules:
        rule = rule.strip()

        match = re.match(r"([\w\s]+?) bags", rule)
        if match:
            parent_bag_color = match.group(1)
        child_bags_contained = re.findall(r"(\d+) ([\w\s]+?) bag", rule)

        GRAPH[parent_bag_color] = child_bags_contained

    return bags_required(COLOR_TO_MATCH) - 1


if __name__ == "__main__":
    print(handler(fileinput.input()))
