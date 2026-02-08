[![Static Analysis](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/pylint.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/pylint.yml)
[![P1: Compute Statistics](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p1-tests.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p1-tests.yml)
[![P2: Convert Numbers](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p2-tests.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p2-tests.yml)
[![P3: Word Count](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p3-tests.yml/badge.svg)](https://github.com/ArtemioPadilla/good-programming-practices/actions/workflows/p3-tests.yml)

# Good Programming Practices

A collection of three Python programs built with a strict emphasis on **code quality**, **coding standards**, and **static analysis** — demonstrating that well-written software is not just functional, but maintainable, readable, and robust.

Each program follows the **PEP-8** coding standard and achieves a perfect **10.00/10** pylint score with zero convention, refactoring, warning, error, or fatal messages.

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

Reads a dataset of numeric values and computes descriptive statistics entirely from first principles — no external libraries, no built-in shortcuts.

| Statistic | Formula |
|---|---|
| Mean | Sum of values / N |
| Median | Middle value of sorted data |
| Mode | Most frequently occurring value |
| Standard Deviation | Population standard deviation (sigma) |
| Variance | Population variance (sigma squared) |

```bash
python computeStatistics.py dataset.txt
```

Results are printed to the console and saved to `StatisticsResults.txt`, including elapsed execution time.

---

### 2. Number Converter

Converts a list of integers into their **binary** and **hexadecimal** representations using manual base-conversion algorithms. Handles both positive and negative integers, applying two's complement notation for negative values.

```bash
python convertNumbers.py dataset.txt
```

Results are printed to the console and saved to `ConvertionResults.txt`, including elapsed execution time.

---

### 3. Word Count

Analyzes a text file to identify every distinct word and its frequency of occurrence, implemented with fundamental data structures and iteration — no specialized counting utilities.

```bash
python wordCount.py dataset.txt
```

Results are printed to the console and saved to `WordCountResults.txt`, including elapsed execution time.

---

## Getting Started

**Prerequisites**

- Python 3.x
- pylint (`pip install pylint`)

**Running a program**

```bash
python <program>.py <input_file>
```

Each program accepts a single file as a command-line argument. Invalid or non-numeric entries in the input are handled gracefully — an error is reported to the console and processing continues with the remaining data.

---

## Quality Assurance

Every program in this repository is validated against two criteria:

**Static Analysis** — Zero issues reported by pylint.

```bash
pylint computeStatistics.py
pylint convertNumbers.py
pylint wordCount.py
```

**Functional Correctness** — All provided test cases produce the expected output.

| Program | Test Cases | Validates |
|---|---|---|
| Compute Statistics | 7 | Integers, floats, large numbers, invalid data |
| Number Converter | 4 | Positive integers, negative integers, invalid entries |
| Word Count | 5 | Small to large files (100–5000 words) |

---

## Project Structure

```
good-programming-practices/
├── .github/workflows/   # CI pipelines (pylint + per-program tests)
├── tests/               # pytest test suite (TDD)
├── P1/
│   ├── source/          # computeStatistics.py
│   ├── tests/           # Test case input files (TC1–TC7)
│   └── results/         # Execution evidence
├── P2/
│   ├── source/          # convertNumbers.py
│   ├── tests/           # Test case input files (TC1–TC4)
│   └── results/         # Execution evidence
├── P3/
│   ├── source/          # wordCount.py
│   ├── tests/           # Test case input files (TC1–TC5)
│   └── results/         # Execution evidence
├── aux/                 # Original test data and expected results
└── README.md
```
