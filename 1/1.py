import fileinput


def handler(expenses):
    expenses = list(map(int, expenses))

    for i in expenses:
        for j in expenses:
            if i + j == 2020:
                return i * j


if __name__ == "__main__":
    print(handler(fileinput.input()))
