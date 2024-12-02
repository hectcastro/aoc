import fileinput
from collections import Counter
from fileinput import FileInput


def handler(raw_lines: FileInput) -> int:
    left_list = []
    right_list = []

    for line in raw_lines:
        left_num_str, right_num_str = line.strip().split()
        left_list.append(int(left_num_str))
        right_list.append(int(right_num_str))

    right_counter = Counter(right_list)

    total_similarity_score = 0
    for num in left_list:
        count_in_right = right_counter.get(num, 0)
        total_similarity_score += num * count_in_right

    return total_similarity_score


if __name__ == "__main__":
    print(handler(fileinput.input()))
