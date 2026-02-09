[![Static Analysis](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/pylint.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/pylint.yml)
[![P1: Compute Statistics](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p1-tests.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p1-tests.yml)
[![P2: Convert Numbers](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p2-tests.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p2-tests.yml)
[![P3: Word Count](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p3-tests.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p3-tests.yml)

# Good Programming Practices

A collection of three Python programs built with a strict emphasis on **code quality**, **coding standards**, and **static analysis** — demonstrating that well-written software is not just functional, but maintainable, readable, and robust.

Each program follows the **PEP-8** coding standard and achieves a perfect **10.00/10** pylint score with zero convention, refactoring, warning, error, or fatal messages.

All computations are implemented from first principles — **no external libraries** and no built-in shortcuts (`math`, `statistics`, `collections.Counter`, `bin()`, `hex()`, etc. are not used).

---

## Table of Contents

- [Programs](#programs)
  - [Compute Statistics](#1-compute-statistics)
  - [Number Converter](#2-number-converter)
  - [Word Count](#3-word-count)
- [Getting Started](#getting-started)
- [Quality Assurance](#quality-assurance)
- [Project Structure](#project-structure)

---

## Programs

### 1. Compute Statistics

Reads a dataset of numeric values and computes descriptive statistics entirely from first principles.

| Statistic | Algorithm |
|---|---|
| Mean | Cumulative sum / N |
| Median | Sort + middle-value selection |
| Mode | Frequency counting with dictionary |
| Variance | Sum of squared differences, N-1 denominator (sample variance) |
| Standard Deviation | Square root via Newton's method, N denominator (population SD) |

```bash
python P1/source/computeStatistics.py P1/tests/TC1.txt
```

```
COUNT: 400
MEAN: 242.32
MEDIAN: 239.5
MODE: 393.0
SD: 145.25810683056557
VARIANCE: 21152.79959899749
Elapsed Time: 0.001287 seconds
```

Invalid entries are reported and skipped without interrupting execution:

```
Error: 'ABA' is not a valid number, skipping.
Error: '23,45' is not a valid number, skipping.
COUNT: 311
MEAN: 241.49511400651465
...
```

Results are saved to `StatisticsResults.txt`.

---

### 2. Number Converter

Converts a list of integers into their **binary** and **hexadecimal** representations using manual base-conversion algorithms.

| Conversion | Algorithm |
|---|---|
| Binary | Successive division by 2; negatives in 10-bit two's complement |
| Hexadecimal | Successive division by 16; negatives in 40-bit two's complement |

```bash
python P2/source/convertNumbers.py P2/tests/TC3.txt
```

```
ITEM    VALUE   BIN          HEX
1       -39     1111011001   FFFFFFFFD9
2       -36     1111011100   FFFFFFFFDC
3       8       1000         8
4       34      100010       22
...
Elapsed Time: 0.001480 seconds
```

Invalid entries are reported and skipped:

```
Error: 'ABC' is not a valid integer, skipping.
```

Results are saved to `ConvertionResults.txt`.

---

### 3. Word Count

Analyzes a text file to identify every distinct word and its frequency of occurrence, sorted by descending frequency then alphabetically.

| Feature | Algorithm |
|---|---|
| Frequency counting | Dictionary-based accumulation (no `collections.Counter`) |
| Sorting | By frequency (descending), then alphabetically (ascending) |

```bash
python P3/source/wordCount.py P3/tests/TC2.txt
```

```
amongst     4
brass       4
chain       4
doc         4
...
advantages  1
afternoon   1
...
Grand Total 184
Elapsed Time: 0.001244 seconds
```

Results are saved to `WordCountResults.txt`.

---

## Getting Started

**Prerequisites**

- Python 3.x
- pylint (`pip install pylint`)
- pytest (`pip install pytest`) — for running the automated test suite

**Running a program**

```bash
python P1/source/computeStatistics.py <input_file>
python P2/source/convertNumbers.py <input_file>
python P3/source/wordCount.py <input_file>
```

Each program accepts a single file as a command-line argument. Invalid or non-numeric entries in the input are handled gracefully — an error is reported to the console and processing continues with the remaining data.

**Using the Makefile**

```bash
make all       # Lint + test everything (default)
make lint      # Run pylint on all 3 programs
make test      # Run all 20 pytest tests
make test-p1   # Run P1 tests only (7 TCs + pylint)
make test-p2   # Run P2 tests only (5 TCs + pylint)
make test-p3   # Run P3 tests only (5 TCs + pylint)
make lint-p1   # Run pylint on computeStatistics.py
make lint-p2   # Run pylint on convertNumbers.py
make lint-p3   # Run pylint on wordCount.py
make clean     # Remove output files and caches
```

---

## Quality Assurance

### Static Analysis

Every program achieves a perfect pylint score:

```
$ pylint P1/source/computeStatistics.py
Your code has been rated at 10.00/10

$ pylint P2/source/convertNumbers.py
Your code has been rated at 10.00/10

$ pylint P3/source/wordCount.py
Your code has been rated at 10.00/10
```

A `.pylintrc` with `module-naming-style=any` allows the required camelCase file names.

### Automated Tests

A `pytest` suite runs each program against all test cases and validates the output:

```
$ make test
======================== 20 passed in 1.22s ========================
```

| Suite | Tests | Result |
|-------|-------|--------|
| P1 — Compute Statistics | 7 functional + 1 pylint | 8/8 pass |
| P2 — Convert Numbers | 5 functional + 1 pylint | 6/6 pass |
| P3 — Word Count | 5 functional + 1 pylint | 6/6 pass |
| **Total** | **20** | **20/20 pass** |

### Continuous Integration

GitHub Actions runs pylint and the full test suite on every push, with separate workflows per program for granular feedback (see badges at the top).

### Test Cases

| Program | TCs | Scale | Invalid data |
|---|---|---|---|
| Compute Statistics | 7 | 400 – 12,769 elements | Yes (TC5, TC7) |
| Number Converter | 4 | 200 elements, range -50 to large positives | Yes (TC4) |
| Word Count | 5 | 100 – 5,000 words | — |

Execution evidence for every test case is stored in `P{n}/results/`.

---

## Project Structure

```
good-programming-practices/
├── P1/
│   ├── source/computeStatistics.py
│   ├── tests/TC1.txt … TC7.txt
│   └── results/                    ← Execution evidence
├── P2/
│   ├── source/convertNumbers.py
│   ├── tests/TC1.txt … TC4.txt
│   └── results/
├── P3/
│   ├── source/wordCount.py
│   ├── tests/TC1.txt … TC5.txt
│   └── results/
├── aux/                            ← Original test data (provided by instructor)
├── tests/                          ← Automated test suite (pytest)
├── .github/workflows/              ← CI/CD pipelines
├── .pylintrc
├── Makefile
├── REPORT.md                       ← Detailed execution report
└── README.md
```

| Folder | Purpose |
|--------|---------|
| `aux/` | Reference input files and expected outputs provided by the instructor. Not modified. |
| `P{n}/source/` | Source code for each program. |
| `P{n}/tests/` | Input files organized per program for independent execution. |
| `P{n}/results/` | Generated outputs serving as documented evidence of successful runs. |
| `tests/` | `pytest` test suite that validates all programs automatically. |
