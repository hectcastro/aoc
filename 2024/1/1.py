import fileinput
from fileinput import FileInput


def handler(raw_lines: FileInput) -> int:
    left_list = []
    right_list = []

    for line in raw_lines:
        left_num_str, right_num_str = line.strip().split()
        left_list.append(int(left_num_str))
        right_list.append(int(right_num_str))

    left_list.sort()
    right_list.sort()

    total_distance = 0
    for left_num, right_num in zip(left_list, right_list):
        total_distance += abs(left_num - right_num)

    return total_distance


if __name__ == "__main__":
    print(handler(fileinput.input()))
