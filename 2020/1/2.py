import fileinput
from fileinput import FileInput


def handler(expenses: FileInput) -> int:
    entries = [int(expense) for expense in expenses]

    for i in entries:
        for j in entries:
            for k in entries:
                if i + j + k == 2020:
                    return i * j * k

    return 0


if __name__ == "__main__":
    print(handler(fileinput.input()))
