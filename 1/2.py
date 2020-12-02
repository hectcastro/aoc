import fileinput


def handler(expenses):
    expenses = list(map(int, expenses))

    for i in expenses:
        for j in expenses:
            for k in expenses:
                if i + j + k == 2020:
                    return i * j * k


if __name__ == "__main__":
    print(handler(fileinput.input()))
