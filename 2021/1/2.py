import fileinput
from fileinput import FileInput

import pandas as pd

WINDOW_SIZE = 3


def handler(raw_measurements: FileInput) -> int:
    measurements = pd.Series([int(measurement) for measurement in raw_measurements])
    measurement_sums = []

    for window_series in measurements.rolling(window=WINDOW_SIZE):
        if len(window_series) == WINDOW_SIZE:
            measurement_sums.append(window_series.sum())

    measurement_sum_increases = 0

    for window_series in pd.Series(measurement_sums).rolling(window=2):
        window = window_series.values

        if len(window) == 2:
            if window[1] > window[0]:
                measurement_sum_increases += 1

    return measurement_sum_increases


if __name__ == "__main__":
    print(handler(fileinput.input()))
