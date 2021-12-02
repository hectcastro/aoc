import fileinput
from fileinput import FileInput

import pandas as pd

WINDOW_SIZE = 2


def handler(raw_measurements: FileInput) -> int:
    measurements = pd.Series([int(measurement) for measurement in raw_measurements])
    measurement_increases = 0

    for window_series in measurements.rolling(window=WINDOW_SIZE):
        window = window_series.values

        if len(window) == WINDOW_SIZE:
            if window[1] > window[0]:
                measurement_increases += 1

    return measurement_increases


if __name__ == "__main__":
    print(handler(fileinput.input()))
