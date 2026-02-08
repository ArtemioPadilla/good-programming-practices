"""Count the frequency of each distinct word in a file."""

import sys
import time


def count_words(filepath):
    """Read words from a file and return a frequency dictionary."""
    frequencies = {}
    with open(filepath, encoding="utf-8") as file_handle:
        for line in file_handle:
            word = line.strip()
            if not word:
                continue
            frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def main():
    """Read words from a file and display their frequencies."""
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py <file>")
        sys.exit(1)

    start_time = time.time()
    frequencies = count_words(sys.argv[1])

    sorted_words = sorted(frequencies.items(),
                          key=lambda item: (-item[1], item[0]))

    total = 0
    for _, count in sorted_words:
        total += count

    elapsed = time.time() - start_time

    lines = []
    for word, count in sorted_words:
        lines.append(f"{word}\t{count}")
    lines.append(f"Grand Total\t{total}")

    for line in lines:
        print(line)
    print(f"Elapsed Time: {elapsed:.6f} seconds")

    with open("WordCountResults.txt", "w", encoding="utf-8") as out_file:
        for line in lines:
            out_file.write(line + "\n")
        out_file.write(f"Elapsed Time: {elapsed:.6f} seconds\n")


if __name__ == "__main__":
    main()
