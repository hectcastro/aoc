import fileinput
from fileinput import FileInput
from typing import List, Set


def handler(answer_sets: FileInput) -> int:
    common_group_answers = []
    unique_group_answers: Set[str] = set()
    group_answers: List[Set[str]] = []

    for answer_set in answer_sets:
        if answer_set == "\n":
            # At the end of a group, intersect each individual group
            # answer set with a set of unique group answers.
            #
            # Finally, add to a global list, with one entry per group.
            common_group_answers.append(len(unique_group_answers.intersection(*group_answers)))
            unique_group_answers.clear()
            group_answers.clear()
            continue

        # Add all answer sets for a given group to a list.
        group_answers.append(set(answer_set.strip()))

        # Add all individual answers within a group to a set to
        # determine those that are unique within a group.
        for answer in answer_set.strip():
            unique_group_answers.add(answer)

    common_group_answers.append(len(unique_group_answers.intersection(*group_answers)))

    return sum(common_group_answers)


if __name__ == "__main__":
    print(handler(fileinput.input()))
