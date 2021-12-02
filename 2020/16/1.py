import re
import sys
from typing import List, TextIO


def parse_rules(raw_rules: str) -> List[int]:
    valid_numbers: List[int] = []

    for start, end in re.findall(r"(\d+)-(\d+)", raw_rules):
        valid_numbers += range(int(start), int(end) + 1)

    return valid_numbers


def parse_tickets(raw_tickets: str) -> List[List[int]]:
    tickets = []

    for raw_ticket in raw_tickets.split("\n")[1:]:
        tickets.append(list(map(int, raw_ticket.split(","))))

    return tickets


def handler(raw_document: TextIO) -> int:
    raw_rules, _, raw_nearby_tickets = raw_document.read().split("\n\n")

    rules = parse_rules(raw_rules)
    tickets = parse_tickets(raw_nearby_tickets.strip())

    ticket_scanning_error_rate = 0

    for ticket in tickets:
        for value in ticket:
            if value not in rules:
                ticket_scanning_error_rate += value
                break

    return ticket_scanning_error_rate


if __name__ == "__main__":
    print(handler(sys.stdin))
