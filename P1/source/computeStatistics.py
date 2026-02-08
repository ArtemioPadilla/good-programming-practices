"""Compute descriptive statistics from a file of numbers."""

import sys
import time


def read_data(filepath):
    """Read data from a file, one entry per line.

    Returns (total_count, valid_numbers) where total_count includes
    invalid entries and valid_numbers is the list of parsed floats.
    """
    total_count = 0
    numbers = []
    with open(filepath, encoding="utf-8") as file_handle:
        for line in file_handle:
            stripped = line.strip()
            if not stripped:
                continue
            total_count += 1
            try:
                numbers.append(float(stripped))
            except ValueError:
                print(f"Error: '{stripped}' is not a valid number, skipping.")
    return total_count, numbers


def compute_mean(numbers):
    """Return the arithmetic mean of a list of numbers."""
    total = 0.0
    for number in numbers:
        total += number
    return total / len(numbers)


def compute_median(numbers):
    """Return the median of a list of numbers."""
    sorted_nums = sorted(numbers)
    length = len(sorted_nums)
    mid = length // 2
    if length % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0
    return sorted_nums[mid]


def compute_mode(numbers):
    """Return the mode, or None if all values are unique."""
    frequency = {}
    for number in numbers:
        frequency[number] = frequency.get(number, 0) + 1
    max_freq = 0
    mode_value = None
    for number, freq in frequency.items():
        if freq > max_freq:
            max_freq = freq
            mode_value = number
    if max_freq <= 1:
        return None
    return mode_value


def compute_variance_and_sd(numbers, mean):
    """Return (sample_variance, population_sd).

    Sample variance uses N-1 denominator.
    Population standard deviation uses N denominator.
    """
    total = 0.0
    for number in numbers:
        total += (number - mean) ** 2
    count = len(numbers)
    population_var = total / count
    sample_var = total / (count - 1)
    return sample_var, compute_sqrt(population_var)


def compute_sqrt(value):
    """Return the square root using Newton's method."""
    if value == 0:
        return 0.0
    guess = value / 2.0
    for _ in range(10000):
        new_guess = (guess + value / guess) / 2.0
        if abs(new_guess - guess) < 1e-15:
            return new_guess
        guess = new_guess
    return guess


def main():
    """Read numbers from a file and compute descriptive statistics."""
    if len(sys.argv) < 2:
        print("Usage: python computeStatistics.py <file>")
        sys.exit(1)

    start_time = time.time()
    count, numbers = read_data(sys.argv[1])

    if not numbers:
        print("Error: no valid numbers found in the file.")
        sys.exit(1)
    mean = compute_mean(numbers)
    median = compute_median(numbers)
    mode = compute_mode(numbers)
    variance, std_dev = compute_variance_and_sd(numbers, mean)
    elapsed = time.time() - start_time

    mode_str = "N/A" if mode is None else str(mode)
    lines = [
        f"COUNT: {count}",
        f"MEAN: {mean}",
        f"MEDIAN: {median}",
        f"MODE: {mode_str}",
        f"SD: {std_dev}",
        f"VARIANCE: {variance}",
        f"Elapsed Time: {elapsed:.6f} seconds",
    ]

    for line in lines:
        print(line)

    with open("StatisticsResults.txt", "w", encoding="utf-8") as out_file:
        for line in lines:
            out_file.write(line + "\n")


if __name__ == "__main__":
    main()
