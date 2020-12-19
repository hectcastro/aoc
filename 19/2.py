import regex  # type: ignore
import sys

from typing import Dict, TextIO

RULES: Dict[int, str] = {}


def expand_rule(rule: str) -> str:
    if rule.isdigit():
        return group_rule_by_index(int(rule))

    return rule


def group_rule_by_index(index: int) -> str:
    return f"(?:{''.join(map(expand_rule, RULES[index].split()))})"


def handler(raw_rules_and_messages: TextIO) -> int:
    raw_rules, raw_messages = raw_rules_and_messages.read().split("\n\n")

    for raw_rule in raw_rules.strip().splitlines():
        index, rule = raw_rule.split(": ")

        if index == "8":
            rule = "42 +"
        elif index == "11":
            rule = "(?P<group> 42 (?&group)? 31 )"

        RULES[int(index)] = rule.replace('"', "")

    rule_zero_matches = 0

    for raw_message in raw_messages.strip().splitlines():
        rule_zero_matches += (
            regex.compile(group_rule_by_index(0)).fullmatch(raw_message) is not None
        )

    return rule_zero_matches


if __name__ == "__main__":
    print(handler(sys.stdin))
