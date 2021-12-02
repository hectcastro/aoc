import fileinput
from fileinput import FileInput
from typing import Set


def handler(answer_sets: FileInput) -> int:
    all_group_answers = []
    unique_group_answers: Set[str] = set()

    for answer_set in answer_sets:
        if answer_set == "\n":
            # At the end of a group, add the number of unique answers
            # to a global list for summation later.
            all_group_answers.append(len(unique_group_answers))
            unique_group_answers.clear()
            continue

        # Add all individual answers within a group to a set to
        # determine those that are unique within a group.
        for answer in answer_set.strip():
            unique_group_answers.add(answer)

    # At the end of all the groups, add the number of unique answers
    # to the global list.
    all_group_answers.append(len(unique_group_answers))

    return sum(all_group_answers)


if __name__ == "__main__":
    print(handler(fileinput.input()))
