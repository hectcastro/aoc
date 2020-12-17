import re
import sys

from collections import defaultdict
from typing import Dict, List, Set, TextIO, Tuple


def parse_rules(raw_rules: str) -> Dict[str, List[int]]:
    rules: Dict[str, List[int]] = defaultdict(list)

    for raw_rule in raw_rules.splitlines():
        field, raw_ranges = raw_rule.split(": ")
        for start, end in re.findall(r"(\d+)-(\d+)", raw_ranges):
            rules[field] += range(int(start), int(end) + 1)

    return rules


def parse_my_ticket(raw_my_ticket: str) -> List[int]:
    return list(map(int, raw_my_ticket.splitlines()[1].split(",")))


def parse_tickets(raw_tickets: str) -> List[List[int]]:
    tickets = []

    for raw_ticket in raw_tickets.split("\n")[1:]:
        tickets.append(list(map(int, raw_ticket.split(","))))

    return tickets


def handler(raw_document: TextIO) -> int:
    raw_rules, raw_my_ticket, raw_nearby_tickets = raw_document.read().split("\n\n")

    rules = parse_rules(raw_rules.strip())
    my_ticket = parse_my_ticket(raw_my_ticket.strip())
    tickets = parse_tickets(raw_nearby_tickets.strip())

    field_freq: List[set] = []
    for _ in range(len(my_ticket)):
        field_freq.append(set())

    for ticket in tickets:
        for index, value in enumerate(ticket):
            fields = set()

            for field, rule in rules.items():
                if value in rule:
                    fields.add(field)

            if fields:
                if field_freq[index]:
                    field_freq[index] = field_freq[index].intersection(fields)
                else:
                    field_freq[index] = fields

    sorted_field_freq: List[Tuple[int, int, Set[str]]] = []
    for index, fields in enumerate(field_freq):
        sorted_field_freq.append((len(fields), index, fields))

    used_fields: Set[str] = set()
    departure_values = 1

    for _, index, fields in sorted(sorted_field_freq):
        field = list(fields.difference(used_fields))[0]

        if field.startswith("departure"):
            departure_values *= my_ticket[index]

        used_fields = used_fields.union(fields)

    return departure_values


if __name__ == "__main__":
    print(handler(sys.stdin))
