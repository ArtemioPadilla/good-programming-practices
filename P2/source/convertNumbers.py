"""Convert numbers from a file to binary and hexadecimal."""

import sys
import time


def to_binary(number):
    """Return the binary string of an integer.

    Negative numbers use 10-bit two's complement.
    """
    if number == 0:
        return "0"
    if number > 0:
        bits = []
        value = number
        while value > 0:
            bits.append(str(value % 2))
            value //= 2
        return "".join(reversed(bits))
    # Negative: 10-bit two's complement
    return to_binary(1024 + number)


def to_hexadecimal(number):
    """Return the hexadecimal string of an integer.

    Negative numbers use 40-bit two's complement.
    """
    hex_digits = "0123456789ABCDEF"
    if number == 0:
        return "0"
    if number > 0:
        chars = []
        value = number
        while value > 0:
            chars.append(hex_digits[value % 16])
            value //= 16
        return "".join(reversed(chars))
    # Negative: 40-bit two's complement (2^40 + number)
    return to_hexadecimal(1099511627776 + number)


def main():
    """Read integers from a file and convert to binary and hex."""
    if len(sys.argv) < 2:
        print("Usage: python convertNumbers.py <file>")
        sys.exit(1)

    start_time = time.time()
    results = []

    with open(sys.argv[1], encoding="utf-8") as file_handle:
        for i, line in enumerate(file_handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                number = int(stripped)
            except ValueError:
                print(f"Error: '{stripped}' is not a valid integer, skipping.")
                continue
            binary = to_binary(number)
            hexadecimal = to_hexadecimal(number)
            results.append(f"{i}\t{number}\t{binary}\t{hexadecimal}")

    elapsed = time.time() - start_time
    header = "ITEM\tVALUE\tBIN\tHEX"
    footer = f"Elapsed Time: {elapsed:.6f} seconds"

    print(header)
    for line in results:
        print(line)
    print(footer)

    with open("ConvertionResults.txt", "w", encoding="utf-8") as out_file:
        out_file.write(header + "\n")
        for line in results:
            out_file.write(line + "\n")
        out_file.write(footer + "\n")


if __name__ == "__main__":
    main()
