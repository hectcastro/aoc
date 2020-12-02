import fileinput

from fileinput import FileInput


def handler(expenses: FileInput) -> int:
    entries = [int(expense) for expense in expenses]

    for i in entries:
        for j in entries:
            if i + j == 2020:
                return i * j

    return 0


if __name__ == "__main__":
    print(handler(fileinput.input()))
